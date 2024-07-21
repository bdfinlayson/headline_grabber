import click

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
    "-i",
    type=click.STRING,
    default=None,
    required=False,
    callback=OptionValidator.validate_site_name,
    help="Comma-separated list of news sources to include in the search",
)
@click.option(
    "--exclude",
    "-e",
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
    is_flag=True,
    default=False,
    help="Launch interactive menu for preference selection",
)
def main(include: str, exclude: str, target_dir: str, limit: int, interactive: bool):
    """Simple program to collect headlines from various news sources and summarize them in a helpful way"""
    if interactive:
        user_preferences = run_interactive_menu()
    else:
        user_preferences = UserPreferences(
            include=(include.split(",") if include else None),
            exclude=(exclude.split(",") if exclude else None),
            target_dir=target_dir if target_dir else None,
            limit=limit if limit else None,
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
    site_abbreviation = [site.abbreviation for site in sites]
    include_exclude_answer = click.prompt(
        'Do you prefer to include certain sites or exclude certain sites?',
        type=click.Choice(['Include', 'Exclude'], case_sensitive=False)
    )
    while True:
        click.echo("Available sites:")
        for site in site_abbreviation:
            click.echo(f" - {site}")
        if include_exclude_answer.lower() == 'include':
            choice_message = 'Which sites would you like to include? (comma-separated)'
        else:
            choice_message = 'Which sites would you like to exclude? (comma-separated)'
        sites_answer = click.prompt(
            choice_message,
            type=str,
            default='',
            show_default=False
        )
        selected_sites = [site.strip() for site in sites_answer.split(',')]
        unique_sites = list(set(selected_sites))
        valid_sites = [site for site in unique_sites if site in site_abbreviation]
        invalid_sites = [site for site in unique_sites if site not in site_abbreviation]
        if invalid_sites:
            click.echo(f"Warning: The following sites are not valid: {', '.join(invalid_sites)}")
        else:
            break
    if include_exclude_answer.lower() == 'include':
        include_sites = valid_sites
        exclude_sites = None
    else:
        include_sites = None
        exclude_sites = valid_sites
    max_results_answer = click.prompt(
        'What is the maximum number of results per subject you\'d like to see?',
        type=int,
        default=None
    )
    custom_directory_answer = click.prompt(
        'Do you have a custom directory you\'d like your HTML reports exported to?',
        type=str,
        default=None
    )
    if include_exclude_answer.lower() == 'include':
        include_sites = valid_sites
        exclude_sites = None
    else:
        include_sites = None
        exclude_sites = valid_sites

    return UserPreferences(
        include=include_sites,
        exclude=exclude_sites,
        target_dir=custom_directory_answer if custom_directory_answer else None,
        limit=max_results_answer if max_results_answer else None
    )

