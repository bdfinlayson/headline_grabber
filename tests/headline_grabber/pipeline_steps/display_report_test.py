import os
import shutil

from datetime import datetime
from headline_grabber.pipeline_steps.display_report import DisplayReport
from tests.headline_grabber.pipeline_steps.test_data.display_report_data import DisplayReportData

def test_build_export_path():
    target_dir = None
    result = DisplayReport.build_export_path(target_dir)
    assert result == os.path.join(os.getcwd(), "reports")
    shutil.rmtree(result, ignore_errors=True)

    target_dir = "/Users/n3t/Documents/COSC540/report0720"
    result = DisplayReport.build_export_path(target_dir)
    assert result == target_dir
    shutil.rmtree(result, ignore_errors=True)

def test_build_html_file_path():
    target_dir = None
    assert "news_report_" in DisplayReport.build_html_file_path(target_dir)

    target_dir = "/Users/n3t/Documents/COSC540/report0720"
    assert "/Users/n3t/Documents/COSC540/report0720/news_report_" in DisplayReport.build_html_file_path(target_dir)

def test_build_html_content():
    context = DisplayReportData.GOOD_CONTEXT
    html_report = DisplayReport().build_html_content(context)
    assert "<title>Dominate your HTML</title>" in html_report
    assert "<h1>Headline Grabber Report</h1>" in html_report
    assert '<button aria-controls="collapse0" aria-expanded="true" class="accordion-button" data-bs-target="#collapse0" data-bs-toggle="collapse" type="button">World</button>' in html_report
    assert "<h4>Braverman claims leadership rival Jenrick is from left of Tory party</h4>" in html_report
    assert "<span>Positive (0.1)</span>" in html_report
    assert '<a href="https://www.thetimes.com/uk/politics/article/suella-braverman-tory-leadership-race-robert-jenrick-rivals-mnghlk9fn">https://www.thetimes.com/uk/politics/article/suella-braverman-tory-leadership-race-robert-jenrick-rivals-mnghlk9fn</a>' in html_report

def test_display_report_fail():
    target_dir = "/Users/n3t/Documents/COSC540/report0720"
    os.makedirs(target_dir, exist_ok=True)
    assert DisplayReport._display_report(DisplayReportData.HTML_CONTENT, target_dir) == False
    shutil.rmtree(target_dir, ignore_errors=True)

def test_display_report_success():
    formatted_datetime = datetime.now().strftime("%Y-%m-%d_%H_%M")
    report_path = "/Users/n3t/Documents/COSC540/report0720"
    os.makedirs(report_path, exist_ok=True)
    report_name = f"/news_report_{formatted_datetime}.html"
    assert DisplayReport._display_report(DisplayReportData.HTML_CONTENT, report_path + report_name) == True
    shutil.rmtree(report_path, ignore_errors=True)

def test_run_success():
    context = DisplayReportData.GOOD_CONTEXT
    DisplayReport().run(context)
    report_path = context.user_input.target_dir
    assert len(os.listdir(report_path)) > 0
    shutil.rmtree(report_path, ignore_errors=True)

def test_sanitize_html_content():
    html_content = "<h4>Braverman claims — ”leadership rival” Jenrick‘ is from left of Tory party</h4>"
    assert DisplayReport.sanitize_html_content(html_content) == "<h4>Braverman claims - \"leadership rival\" Jenrick' is from left of Tory party</h4>"  