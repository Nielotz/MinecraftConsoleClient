import logging
logger = logging.getLogger("mainLogger")

from action.move_manager import MoveManager

COMMAND = {}  # Needs to be initialized.


def interpret(bot, raw_input: str):
    """
    TODO: Optimize (when chat interpretation will be ready), add comment.

    :param bot: Bot where apply interpreted stuff
    :param raw_input: str from which to extract command
    """

    raw_input = raw_input.replace("'", "")\
                         .replace("}", "")\
                         .replace("{", "")\
                         .replace("[", "")\
                         .replace("]", "")\
                         .replace(",", "")

    words = raw_input.split()
    for command_name in COMMAND:
        if command_name not in words:
            continue

        command_idx = words.index(command_name)
        command = COMMAND[command_name]
        subcommand_idx = command_idx + 1
        try:
            subcommand = command[words[subcommand_idx]]
        except (IndexError, KeyError):
            logger.warning("Invalid subcommand")
            break

        offset = 1
        args = []
        try:
            for arg_type in subcommand.args_types:
                args.append(arg_type(words[subcommand_idx + offset]
                                     .replace("'", "")
                                     .replace("}", "")
                                     .replace("]", "")
                                     .replace(",", "")))
                offset += 1
        except (KeyError, ValueError, IndexError):
            print(words[subcommand_idx + offset])
            logger.warning("Invalid arguments")
            break
        subcommand.func(bot, *args)
        break


def __goto(bot, x: float, y: float, z: float):
    move_manager: MoveManager = bot.move_manager
    move_manager.add_target(x, y, z)


def __goto_clear(bot):
    move_manager: MoveManager = bot.move_manager
    move_manager.clear_targets()


def __pause(bot):
    move_manager: MoveManager = bot.move_manager
    move_manager.pause()


def __resume(bot):
    move_manager: MoveManager = bot.move_manager
    move_manager.resume()


def __skip(bot):
    move_manager: MoveManager = bot.move_manager
    move_manager.skip_actual_target()
