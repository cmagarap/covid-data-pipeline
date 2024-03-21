from datetime import datetime, timedelta

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # last_update = kwargs.get('execution_date')
    last_update = datetime.strptime('2020-06-07', '%Y-%m-%d')
    last_update += timedelta(days=1)
    last_update_str = last_update.strftime('%Y-%m-%d')
    print(last_update_str)
    # Remove duplicate rows
    data = data.drop_duplicates()
    
    data['Last_Update'] = data['Last_Update'].astype(str)
    # Only get the last_update for the [current date]
    data = data[data['Last_Update'].str.split(' ').str[0] == last_update_str]

    return len(data)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
