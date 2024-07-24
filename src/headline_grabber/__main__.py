import click
from PyInquirer import prompt, Separator
from headline_grabber.configurations.sites import sites
from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.models.user_preferences import UserPreferences
from headline_grabber.pipelines import news_pipeline
from headline_grabber.validators.click.option_validator import OptionValidator


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
    )
)
@click.option(
    "--include",
    "-inc",
    type=click.STRING,
    default=None,
    required=False,
    callback=OptionValidator.validate_site_name,
    help="Comma-separated list of news sources to include in the search",
)
@click.option(
    "--exclude",
    "-exc",
    type=click.STRING,
    default=None,
    required=False,
    callback=OptionValidator.validate_site_name,
    help="Comma-separated list of news sources to exclude from the search",
)
@click.option(
    "--target-dir",
    "-td",
    type=click.STRING,
    default=None,
    required=False,
    callback=OptionValidator.validate_target_dir,
    help="The target directory where html news reports should be exported to",
)
@click.option(
    "--limit",
    "-l",
    type=int,
    default=None,
    required=False,
    callback=OptionValidator.validate_max_entries,
    help="Number specifying the maximum number of entries per topic in a report",
)
@click.option(
    "--interactive",
    "-i",
    is_flag=True,
    default=False,
    help="Launch interactive menu for preference selection",
)
@click.option(
    "--filter-sentiment",
    "-f",
    type=str,
    default=None,
    required=False,
    callback=OptionValidator.validate_filter_sentiment,
    help="Filters out news headlines ranked positive or negative based on entered value of positive or negative",
)
  
def main(include: str, exclude: str, target_dir: str, limit: int, filter_sentiment: str, interactive: bool):
    """Simple program to collect headlines from various news sources and summarize them in a helpful way"""
    if interactive:
        user_preferences = run_interactive_menu()
    else:
        user_preferences = UserPreferences(
            include=(include.split(",") if include else None),
            exclude=(exclude.split(",") if exclude else None),
            target_dir=target_dir if target_dir else None,
            limit=limit if limit else None,
            filter_sentiment=(filter_sentiment if filter_sentiment else None),
        )
    pipeline_context = PipelineContext(
        site_configs=sites,
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=user_preferences,
        )

    pipeline_context = news_pipeline.run(pipeline_context)

def run_interactive_menu() -> UserPreferences:
    site_abbreviations = [site.abbreviation for site in sites]
    include_exclude_answer = prompt({
        'type': 'list',
        'name': 'include_exclude',
        'message': 'Do you prefer to include or exclude certain sites?',
        'choices': ['Include', 'Exclude']
    })['include_exclude']

    site_answers = prompt({
        'type': 'checkbox',
        'name': 'sites',
        'message': 'Select sites (use space to select/deselect):',
        'choices': [{'name': site} for site in site_abbreviations],
        'validate': lambda answer: 'You must choose at least one site.' if len(answer) == 0 else True
    })['sites']
    click.echo(f"Selected sites: {', '.join(site_answers)}")
    
    max_results = prompt({
        'type': 'input',
        'name': 'max_results',
        'message': 'What is the maximum number of results per subject you\'d like to see?',
        'default': '',
        'validate': lambda val: val.isdigit() or 'Please enter a valid number'
    })['max_results']

    target_dir = prompt({
        'type': 'input',
        'name': 'target_dir',
        'message': 'Do you have a custom directory you\'d like your HTML reports exported to?',
        'default': '',
    })['target_dir']

    include_sites = site_answers if include_exclude_answer == 'Include' else None
    exclude_sites = site_answers if include_exclude_answer == 'Exclude' else None
    if not include_sites and not exclude_sites:
        click.echo("Error: You must select at least one site.")
        return run_interactive_menu()
    unique_sites = list(set(site_answers))
    if len(unique_sites) != len(site_answers):
        click.echo("Error: Duplicate sites selected. Please select unique sites.")
        return run_interactive_menu()
    return UserPreferences(
        include=include_sites,
        exclude=exclude_sites,
        target_dir=target_dir if target_dir else None,
        limit=int(max_results) if max_results else None
    )