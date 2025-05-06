from django.test import TestCase
from django.urls import reverse
from .models import Report

class ReportEditTest(TestCase):
    def setUp(self):
        # テスト用のダミーレコードを作る
        self.report = Report.objects.create(
            title="元のタイトル",
            content="元の内容",
            date="2025-05-06"
        )

    def test_empty_fields_should_show_error(self):
        response = self.client.post(
            reverse('report_edit', args=[self.report.id]),
            data={'title': '', 'content': '', 'date': ''}
        )
        # エラー文が返ってくるかチェック
        self.assertContains(response, "すべての項目を入力してください。")

        # データが変更されていないか確認
        self.report.refresh_from_db()
        self.assertEqual(self.report.title, "元のタイトル")
