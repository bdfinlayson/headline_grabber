import click
from simple_term_menu import TerminalMenu

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
    site_abbreviations = [site.abbreviation for site in sites]

    # include_exclude_answer = click.prompt(
    #     'Do you prefer to include certain sites or exclude certain sites?',
    #     type=click.Choice(['Include', 'Exclude'], case_sensitive=False)
    # ).lower()
    include_exclude_menu_options = ['Include', 'Exclude']
    include_exclude_menu = TerminalMenu(include_exclude_menu_options, multi_select=False)
    incl_excl_idx = include_exclude_menu.show()
    include_exclude_answer = include_exclude_menu_options[incl_excl_idx].lower()
    print(include_exclude_answer)

    while True:
        print("Available sites:")
        terminal_menu = TerminalMenu(site_abbreviations, multi_select=True, show_multi_select_hint=True)
        selected_indices = terminal_menu.show()

        if selected_indices is None:
            click.echo("No sites selected. Please select at least one site.")
            continue

        valid_sites = [site_abbreviations[i] for i in selected_indices]
        print(valid_sites)
        break

    max_results_options = [str(i) for i in range(1, 11)]
    terminal_menu_max_results = TerminalMenu(max_results_options, title="Select the maximum number of results per subject")
    max_results_index = terminal_menu_max_results.show()
    max_results_answer = int(max_results_options[max_results_index]) if max_results_index is not None else None
    print(max_results_answer)

    # Using input for custom_directory_answer but allowing empty input
    custom_directory_answer = input(
        'Do you have a custom directory you\'d like your HTML reports exported to? (press Enter to skip): '
    ).strip()
    custom_directory_answer = custom_directory_answer or None

    if include_exclude_answer == 'include':
        include_sites = valid_sites
        exclude_sites = None
    else:
        include_sites = None
        exclude_sites = valid_sites

    return UserPreferences(
        include=include_sites,
        exclude=exclude_sites,
        target_dir=custom_directory_answer,
        limit=max_results_answer if max_results_answer else None
    )