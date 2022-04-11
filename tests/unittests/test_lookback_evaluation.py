import unittest
from unittest import mock
from tap_stripe import IMMUTABLE_STREAM_LOOKBACK, evaluate_start_time_based_on_lookback, Context, utils

class TestLookbackEvaluation(unittest.TestCase):

    def test_lookback_evaluation_for_no_bookmark_events(self):
        stream_name = "events"
        replication_key = "created"
        config = { "client_secret": "test_secret", "account_id": "test_account", "start_date": "2022-03-30T00:00:00"}
        Context.config = config
        Context.state = {}
        start_window = evaluate_start_time_based_on_lookback(stream_name, replication_key, IMMUTABLE_STREAM_LOOKBACK)
        self.assertEqual(start_window, utils.strptime_to_utc(Context.config['start_date']).timestamp())
    
    def test_lookback_evaluation_for_no_bookmark_balance_transactions(self):
        stream_name = "balance_transactions"
        replication_key = "created"
        config = { "client_secret": "test_secret", "account_id": "test_account", "start_date": "2022-03-30T00:00:00"}
        Context.config = config
        Context.state = {}
        start_window = evaluate_start_time_based_on_lookback(stream_name, replication_key, IMMUTABLE_STREAM_LOOKBACK)
        self.assertEqual(start_window, utils.strptime_to_utc(Context.config['start_date']).timestamp())


    @mock.patch("tap_stripe.dt_to_epoch")
    def test_lookback_evaluation_when_recent_bookmark_events(self, mock_now):
        stream_name = "events"
        replication_key = "created"
        now_time = 1648739354
        state = {'bookmarks': {'events': {'created': 1648739554}}} # 2022-03-31T08:42:34
        config = { "client_secret": "test_secret", "account_id": "test_account", "start_date": "2022-03-30T00:00:00"}
        Context.config = config
        Context.state = state
        start_window = evaluate_start_time_based_on_lookback(stream_name, replication_key, IMMUTABLE_STREAM_LOOKBACK)
        self.assertEqual(start_window, Context.state['bookmarks'][stream_name][replication_key] - IMMUTABLE_STREAM_LOOKBACK)

    @mock.patch("tap_stripe.dt_to_epoch")
    def test_lookback_evaluation_when_recent_bookmark_balance_transactions(self, mock_now):
        stream_name = "balance_transactions"
        replication_key = "created"
        state = {'bookmarks': {'balance_transactions': {'created': 1648739554}}} # 2022-03-31T08:42:34
        config = { "client_secret": "test_secret", "account_id": "test_account", "start_date": "2022-03-30T00:00:00"}
        Context.config = config
        Context.state = state
        start_window = evaluate_start_time_based_on_lookback(stream_name, replication_key, IMMUTABLE_STREAM_LOOKBACK)
        self.assertEqual(start_window,Context.state['bookmarks'][stream_name][replication_key] - IMMUTABLE_STREAM_LOOKBACK)