import logging
import queue
import threading
import time
from contextlib import contextmanager

from data_structures.hero import Hero
from data_structures.position import Position

logger = logging.getLogger("mainLogger")


class MoveManager:
    """Starts new thread as daemon which add moving packets into send_queue"""

    # Returns True / False. Does not indicate whether move_manager has started.
    is_paused: callable = None
    _move_speed: (int, int, int) = None  # (x, y, z)

    _mover: threading.Thread = None
    _started_thread: threading.Event = None
    _target_queue: queue.Queue = None
    _paused: threading.Lock = None
    _skip: bool = None
    __login_packet_creator = None  # Module, read-only.

    _on_pause: [callable, ] = None

    def __init__(self,
                 send_queue: queue.Queue,
                 play_packet_creator,
                 player_data_holder: Hero):
        """
        :param send_queue: queue from where packet will be taken and send
        :param play_packet_creator: module containing actions for moving
        :type player_data_holder: Player object which will be moved
        """
        logger.debug("Starting mover.")

        self._target_queue = queue.Queue()
        self._started_thread = threading.Event()
        self._play_packet_creator = play_packet_creator

        self._paused = threading.Lock()
        self.is_paused = self._paused.locked
        self._skip = False

        self._on_pause = []

        # Started as daemon because of:
        #   1. no need of keeping alive when main ends
        #   2. lack of stop method.
        self._mover = threading.Thread(target=self._handle_moving,
                                       args=(send_queue,
                                             self._target_queue,
                                             player_data_holder),
                                       daemon=True
                                       )

    def start(self) -> bool:
        """
        Starts new daemon that allows complex moving.

        :returns started successfully
        """
        if self._mover.is_alive():
            raise RuntimeError("handle_moving has been already started")

        self._mover.start()
        self._started_thread.wait(15)  # Wait for thread to initialize.

        logger.info("Started mover.")

        return self._mover.is_alive()

    def stop(self):
        """Stops moving thread."""
        self.clear_targets()
        self._target_queue.put(None)

        logger.info("Stopping move manager...")

    def pause(self):
        """Pauses moving. When pausing already paused, nothing will happen."""
        if not self._paused.locked():
            self._paused.acquire()

    def resume(self):
        """Resumes moving. When resuming not paused, nothing will happen."""
        if self._paused.locked():
            self._paused.release()

    @contextmanager
    def __pause_lock(self):
        self.pause()
        yield True
        self.resume()

    def add_target(self,
                   x: float = None, y: float = None, z: float = None,
                   target: Position = None):
        """Adds target position to the goto queue."""
        if target is None:
            target = Position(x, y, z)

        self._target_queue.put(target)

        logger.info(f"Added new target to the goto queue: {target}")

    def skip_actual_target(self):
        self._on_pause.append(self.resume)
        self._skip = True
        self.pause()

    def clear_targets(self):
        """
        Pauses the player. Clears targets. Resumes mover.
        Does not remove 'stop' target - eg. when 'stop' target in queue lefts it.
        """

        logger.info("Clearing targets")

        # Not sure is necessary, but little cost for avoiding weird behaviour.
        with self.__pause_lock():
            stop = False

            while not self._target_queue.empty():
                try:
                    if self._target_queue.get(timeout=3) is None:
                        stop = True
                except TimeoutError:
                    stop = True
                    logger.critical("Can't empty targets.")
                    break

            if stop:
                self._target_queue.put(None)

    def wait_for_resume(self):
        self._paused.acquire()
        self._paused.release()

    def _handle_moving(self,
                       send_queue: queue.Queue,
                       target_queue: queue.Queue,
                       player: Hero):
        """
        Handles moving to targets given in a target_queue.
        Thread shuts down when:
            put target 'None' into queue e.g. when 'target_queue.get() is None',
            main thread ends (daemon thread)
        """
        # This function is not the best one.

        self._started_thread.set()
        logger.debug("Started handling moving")

        """Maximal step distance in one step. Max 0.02. """
        max_step_x: float = 0.02
        max_step_y: float = 0.02
        max_step_z: float = 0.02

        """Move speed blocks / second. Default 0.7. """
        move_speed_x: float = 0.7
        move_speed_y: float = 0.7
        move_speed_z: float = 0.7

        """Amount of steps(packets) per sec. Max 20. """
        steps_per_second: float = sorted((move_speed_x / max_step_x,
                                          move_speed_y / max_step_y,
                                          move_speed_z / max_step_z),
                                         key=float
                                         )[-1]  # Take biggest element.

        if steps_per_second > 20:
            steps_per_second = 20

        """Minimal delay between movement packets equals 50ms. """
        step_delay: float = 1 / steps_per_second

        while True:
            target = target_queue.get()
            if target is None:
                break  # Exit thread loop
            target_x, target_y, target_z = target
            while player.position is None:
                logger.info(f"Waiting for player position.")
                time.sleep(0.2)  # Wait until server sends player position.

            logger.info(f"Actual position: {player.position}")
            logger.info(f"Going to: {target}")

            # Speed is critical.
            create_step_packet = self._play_packet_creator.player_position
            send_packet = send_queue.put
            get_perf_time = time.perf_counter
            is_paused = self._paused.locked

            last_packet_time: float = get_perf_time()

            # TODO: optimize delay_between_packets.
            while True:  # For pause / resume.
                while not is_paused():
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
                        logger.info(f"Reached target {target}")
                        break

                    # print(f"step: {step_x, step_y, step_z}")
                    # print(f"player_pos: {player_pos}")

                    next_player_pos_x = player_pos_x + step_x
                    next_player_pos_y = player_pos_y + step_y
                    next_player_pos_z = player_pos_z + step_z

                    """Packet may be delayed due to full send queue, 
                    and extremely slow connection. """
                    # TODO: Add to the connection priority queue.
                    send_packet(
                        create_step_packet((next_player_pos_x,
                                            next_player_pos_y,
                                            next_player_pos_z),
                                           on_ground=False))

                    player.position.pos = {'x': next_player_pos_x,
                                           'y': next_player_pos_y,
                                           'z': next_player_pos_z}

                    # print(f"player_pos: {player.position.pos}")

                    time.sleep(step_delay -
                               (
                                       get_perf_time() - last_packet_time) % step_delay)
                    last_packet_time: float = get_perf_time()
                else:
                    logger.info(f"Paused moving: {target}")

                    for func in self._on_pause:
                        func()

                    self.wait_for_resume()

                    if not self._skip:
                        logger.info(f"Resumed moving: {target}")
                        continue  # Hit when resumed moving.
                    self._skip = False
                    logger.info(f"Skipped: {target}")
                break

        logger.debug("Stopped move manager.")
