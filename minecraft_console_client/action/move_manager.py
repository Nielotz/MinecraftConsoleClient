import logging

logger = logging.getLogger("mainLogger")

import threading
import queue
import time

from data_structures.player import Player
from data_structures.position import Position


class MoveManager:
    """ Starts new thread as daemon which add moving packets into send_queue """
    __mover: threading.Thread = None
    __started_thread: threading.Event = None
    __target_queue: queue.Queue = None
    _paused: bool = None
    _move_speed: (int, int, int) = None  # (x, y, z)
    __login_packet_creator = None  # Module for use only.

    def __init__(self,
                 send_queue: queue.Queue,
                 play_packet_creator,
                 player: Player):
        """
        :param send_queue: queue from where packet will be taken and send
        :param play_packet_creator: module containing actions for moving
        :type player: Player object which will be moved
        """
        logger.debug("Starting mover.")
        self.__target_queue = queue.Queue()
        self.__started_thread = threading.Event()
        self.__play_packet_creator = play_packet_creator

        # Started as daemon because of:
        #   1. no need of keeping alive when main ends
        #   2. lack of stop method.
        self.__mover = threading.Thread(target=self.__handle_moving,
                                        args=(send_queue,
                                              self.__target_queue,
                                              player),
                                        daemon=True
                                        )
        self._paused = True

    def start(self):
        """ Starts new daemon that allows complex moving. """
        if self.__mover.is_alive():
            raise RuntimeError("handle_moving has been already started")

        if not self._paused:
            raise RuntimeError("handle_moving has been already started")

        self._paused = False
        self.__mover.start()
        self.__started_thread.wait(15)

    def stop(self):
        """ Stops moving thread."""
        self.clear_targets()
        self.__target_queue.put(None)
        logger.debug("Stopping move manager")

    def pause(self):
        """ Pauses moving. """
        self._paused = True

    def resume(self):
        """ Resumes moving. """
        self._paused = False

    def add_target_position(self, target: Position):
        """ Add target position {'x': x, 'y': y, 'z': z} to the goto queue. """
        self.__target_queue.put(target)
        logger.debug(f"Added new target to the goto queue: {target}")

    def clear_targets(self):
        """ Clear target queue. Does not stop player. """
        logger.debug("Clearing targets")
        self._paused = True

        while not self.__target_queue.empty():
            self.__target_queue.get(timeout=2)

    def __handle_moving(self,
                        send_queue: queue.Queue,
                        target_queue: queue.Queue,
                        player: Player):
        """
        Handle moving to targets given in a target_queue.
        Thread shuts down when:
            put target 'None' into queue e.g. when 'target_queue.get() is None',
            main thread ends (daemon thread)
        """

        self.__started_thread.set()
        logger.debug("Started handling moving")

        """ Maximal step distance in one step. Max 0.02. """
        max_step_x: float = 0.02
        max_step_y: float = 0.02
        max_step_z: float = 0.02

        """ Move speed blocks / second. Default 0.7. """
        move_speed_x: float = 0.7
        move_speed_y: float = 0.7
        move_speed_z: float = 0.7

        """ Amount of steps(packets) per sec. Max 20. """
        steps_per_second: float = sorted((move_speed_x / max_step_x,
                                          move_speed_y / max_step_y,
                                          move_speed_z / max_step_z),
                                         key=float
                                         )[-1]  # Take biggest element.

        if steps_per_second > 20:
            steps_per_second = 20

        """ Minimal delay between movement packets equals 50ms."""
        step_delay: float = 1 / steps_per_second

        while True:
            create_step_packet = self.__play_packet_creator.player_position
            send_packet = send_queue.put
            get_perf_time = time.perf_counter

            target = target_queue.get()
            if target is None:
                break  # Exit thread loop
            target_x, target_y, target_z = target.get_list()

            while player.position is None:
                logger.info("Waiting for player position.")
                time.sleep(0.2)  # Wait until server sends player position.

            logger.info(f"Actual position: {player.position}")
            logger.info(f"Going to: {target}")

            last_packet_time: float = get_perf_time()
            # Speed is critical.
            # TODO: optimize delay_between_packets.
            while not self._paused:
                player_pos = player.position.pos
                player_pos_x = player_pos['x']
                player_pos_y = player_pos['y']
                player_pos_z = player_pos['z']

                step_x: float = target_x - player_pos_x
                step_y: float = target_y - player_pos_y
                step_z: float = target_z - player_pos_z

                if step_x < -max_step_x:
                    step_x = -max_step_x
                elif step_x > max_step_x:
                    step_x = max_step_x

                if step_y < -max_step_y:
                    step_y = -max_step_y
                elif step_y > max_step_y:
                    step_y = max_step_y

                if step_z < -max_step_z:
                    step_z = -max_step_z
                elif step_z > max_step_z:
                    step_z = max_step_z

                # Precision based on standard client (F3 info)
                if not (step_x > 0.001 or step_x < -0.001 or
                        step_y > 0.001 or step_y < -0.001 or
                        step_z > 0.00001 or step_z < -0.00001):
                    logger.info(f"Reached target {target.pos}")
                    break

                # print(f"step: {step_x, step_y, step_z}")
                # print(f"player_pos: {player_pos}")

                next_player_pos_x = player_pos_x + step_x
                next_player_pos_y = player_pos_y + step_y
                next_player_pos_z = player_pos_z + step_z

                """ Packet may be delayed due to full send queue, 
                and extremely slow connection. """
                # TODO: Add to the connection second queue with higher priority.
                send_packet(
                   create_step_packet((next_player_pos_x,
                                       next_player_pos_y,
                                       next_player_pos_z),
                                      on_ground=False))

                player.position.pos = {'x': next_player_pos_x,
                                       'y': next_player_pos_y,
                                       'z': next_player_pos_z}

                #print(f"player_pos: {player.position.pos}")

                time.sleep(step_delay -
                           (get_perf_time() - last_packet_time) % step_delay)
                last_packet_time: float = get_perf_time()

        logger.debug("Stopped handling moving")

