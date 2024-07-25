
from headline_grabber.models.display_document import DisplayDocument
from headline_grabber.models.headline import Classification
from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.models.user_preferences import UserPreferences


class DisplayReportData:

    GOOD_CONTEXT = PipelineContext(
        site_configs=[],
        headlines=[],
        grouped_headlines={},
        documents_for_display={
            "World": [
                DisplayDocument(
                    links=[
                        "https://www.thetimes.com/uk/politics/article/suella-braverman-tory-leadership-race-robert-jenrick-rivals-mnghlk9fn",
                    ],
                    summarized_title="Braverman claims leadership rival Jenrick is from left of Tory party",
                    summarized_description='Suella Braverman has accused Robert Jenrick of being a "centrist Rishi supporter" who is "from the left of the party", after one of her key supporters switched to backing the former immigration minister. Jenrick and Braverman, the former home secretary, are among seven of the remaining 121 Tory MPs preparing to stand for the leadership...',
                    average_sentiment=Classification("Positive", 0.1),
                    subjects=[
                        "First Subject",
                    ],
                    most_common_subject="World"
                )
            ]
        },
        user_input=UserPreferences(
            include="nyt",
            exclude=None,
            target_dir="/Users/n3t/Documents/COSC540/report0720",
            limit=None,
        )
    )

    HTML_CONTENT = r'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dominate your HTML</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js" type="text/javascript"></script>
        </head>
        <body>
            <div class="container">
            <div class="row">
                <div class="col-12">
                <h1>Headline Grabber Report</h1>
                <div class="fst-italic">
                    <p>Generated At: 2024-07-21_23_01</p>
                    <p>This report contains content from the following news sources: </p>
                </div>
                </div>
            </div>
            <div class="row">
                <h2>World</h2>
                <div class="col-6">
                <h4>Braverman claims leadership rival Jenrick is from left of Tory party</h4>
                <p>Suella Braverman has accused Robert Jenrick of being a “centrist Rishi supporter” who is “from the left of the party”, after one of her key supporters switched to backing the former immigration minister. Jenrick and Braverman, the former home secretary, are among seven of the remaining 121 Tory MPs preparing to stand for the leadership...</p>
                <b>Sentiment:
                    <span>Positive (0.1)</span>
                </b>
                <p>
                    <b>Sources:</b>
                </p>
                <ol>
                    <li>
                    <a href="https://www.thetimes.com/uk/politics/article/suella-braverman-tory-leadership-race-robert-jenrick-rivals-mnghlk9fn">https://www.thetimes.com/uk/politics/article/suella-braverman-tory-leadership-race-robert-jenrick-rivals-mnghlk9fn</a>
                    </li>
                </ol>
                </div>
                <hr>
            </div>
            </div>
        </body>
        </html>
    '''