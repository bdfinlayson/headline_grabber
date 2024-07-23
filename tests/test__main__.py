from unittest.mock import patch, call, ANY
from click.testing import CliRunner
from headline_grabber.configurations.sites import sites

@patch('PyInquirer.prompt')
@patch('headline_grabber.pipelines.news_pipeline.run')
def test_interactive_mode(mock_pipeline_run, mock_prompt):
    mock_prompt.side_effect = [
        {'include_exclude': 'Include'},
        {'sites': ['nyt', 'wsj']},
        {'max_results': '10'},
        {'target_dir': r'C:\UTK\Advanced_Software_Engineering\headline_grabber_reports'}
    ]
    from headline_grabber.__main__ import main
    cli_runner = CliRunner()
    result = cli_runner.invoke(main, ['--interactive'])
    mock_pipeline_run.assert_called_once()
    assert result.exit_code == 0
    assert 'Selected sites: nyt, wsj' in result.output.strip()
    expected_calls = [
        call({
            'type': 'list',
            'name': 'include_exclude',
            'message': 'Do you prefer to include or exclude certain sites?',
            'choices': ['Include', 'Exclude']
        }),
        call({
            'type': 'checkbox',
            'name': 'sites',
            'message': 'Select sites (use space to select/deselect):',
            'choices': [{'name': site.abbreviation} for site in sites], 
            'validate': ANY  
        }),
        call({
            'type': 'input',
            'name': 'max_results',
            'message': 'What is the maximum number of results per subject you\'d like to see?',
            'default': '',
            'validate': ANY
        }),
        call({
            'type': 'input',
            'name': 'target_dir',
            'message': 'Do you have a custom directory you\'d like your HTML reports exported to?',
            'default': '',
        })
    ]
    for expected, actual in zip(expected_calls, mock_prompt.call_args_list):
        assert expected == actual
    actual_site_choices = next(call[0][0]['choices'] for call in mock_prompt.call_args_list if 'type' in call[0][0] and call[0][0]['type'] == 'checkbox')
    expected_site_choices = [{'name': site.abbreviation} for site in sites]
    assert actual_site_choices == expected_site_choices

    max_results_prompt = next(call[0][0] for call in mock_prompt.call_args_list if call[0][0]['name'] == 'max_results')
    assert max_results_prompt == {
        'type': 'input',
        'name': 'max_results',
        'message': 'What is the maximum number of results per subject you\'d like to see?',
        'default': '',
        'validate': ANY
    }

    target_dir_prompt = next(call[0][0] for call in mock_prompt.call_args_list if call[0][0]['name'] == 'target_dir')
    assert target_dir_prompt == {
        'type': 'input',
        'name': 'target_dir',
        'message': 'Do you have a custom directory you\'d like your HTML reports exported to?',
        'default': '',
    }
    assert mock_pipeline_run.call_args[0][0].user_input.include == ['nyt', 'wsj']
    assert mock_pipeline_run.call_args[0][0].user_input.exclude == None
    assert mock_pipeline_run.call_args[0][0].user_input.limit == 10
    assert mock_pipeline_run.call_args[0][0].user_input.target_dir == r'C:\UTK\Advanced_Software_Engineering\headline_grabber_reports'