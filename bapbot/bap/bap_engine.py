## Imports


# Scientific computing
import bokeh

# Project
from .. import database as db
from .. import utils
from .bap import Bap
from .level import Level
from .player import Player



class BapEngine(object):


    def __init__(self):
        """
        """
        self._sql_handle = db.database.SQLHandle.get_create()

    def _check_register_player(self, player_name):
        """
        """
        player = db.functions.get_player(self._sql_handle, player_name)
        if len(player) == 0:
            join_date = utils.get_timestamp()
            new_player = Player.get_new_player(player_name, join_date)
            db.functions.register_new_player(self._sql_handle, new_player.name, new_player.join_date, new_player.level, new_player.experience)

    def _bap_allowed(self, player_name, bap_type, timestamp):
        """
        """
        # Check player can perform bap
        date = timestamp.date()
        baps_today = db.functions.get_baps(
            self._sql_handle, bapper=player_name, bap_type=bap_type, date_dt=date)
        player = Player(*db.functions.get_player(self._sql_handle, player_name))
        level = Level(*db.functions.get_level(self._sql_handle, player.level))

        bap_limit = level.get_daily_bap_limit(bap_type)

        if len(baps_today) >= level.get_daily_bap_limit(bap_type):
            return False
        else:
            return True

    def _execute_bap(self, bapper, bappee, bap_type, timestamp):
        """
        """
        db.functions.log_bap(self._sql_handle, bapper, bappee, bap_type, timestamp)

    def attempt_bap(self, bapper, bappee, bap_type, timestamp):
        """
        """

        if isinstance(timestamp, str):
            timestamp = utils.timestamp_str_to_timestamp(timestamp)

        self._check_register_player(bapper)
        self._check_register_player(bappee)

        if self._bap_allowed(bapper, bap_type, timestamp):
            self._execute_bap(bapper, bappee, bap_type, timestamp)
            baps = [Bap(*bap) for bap in db.functions.get_baps(
                self._sql_handle, bappee=bappee, date_dt=utils.get_today_date())]

            bap_count = {BAP_TYPE: 0 for BAP_TYPE in Bap.BAP_TYPES}

            for bap in baps:
                bap_count[bap.type] += 1



            return {'bap': 'success', 'baps_today': bap_count}

        else:
            return {'bap': 'fail'}


    def _get_bapper_stats_plot(self):
        """
        """
        bapper_bap_counts = db.functions.get_bap_counts_by_bapper(self._sql_handle)
        bappers = [ele[0] for ele in bapper_bap_counts]
        bap_counts = [ele[1] for ele in bapper_bap_counts]
        plot_html = plots.create_bapper_stats_plot(bappers, bap_counts)
        return plot_html


    def get_stats_plot(self):
        """
        """
        plot_html = self._get_bapper_stats_plot()

        return plot_html
