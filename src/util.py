from collections.abc import Iterator

class UserInputError(Exception):
    pass

def validate_todo(content):
    """
    TODO change the behaviour of this function to validate references. 
    Also remember to change the import statements in app.py and tests.
    
    Validates the content of a todo item. 
    Usage:
        content = request.form.get("content")

         try:
             validate_todo(content)
    """
    if len(content) < 5:
        raise UserInputError("Todo content length must be greater than 4")

    if len(content) > 100:
          raise UserInputError("Todo content length must be smaller than 100")


def is_valid_reference(
        maybe_reference: dict[str: list[str]|str|int]
) -> bool:
    required_keys = [
        "year",
        "author",
        "title",
        "type"
    ]

    validator_iter: Iterator[bool] = map(
        lambda x: _is_valid_reference_helper(
            maybe_reference, x
        ),
        required_keys
    )
    return all(validator_iter)

def _is_valid_reference_helper(
        maybe_reference: dict[str: list[str]],
        key: str
) -> bool:
    if key in maybe_reference.keys()\
       and maybe_reference[key] is not []:
        return True
    else:
        return False
