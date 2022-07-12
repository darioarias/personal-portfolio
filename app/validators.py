from peewee_validates import ModelValidator, StringField, IntegerField, DateTimeField, validate_not_empty, validate_required, validate_email


class TimelinePostValidator(ModelValidator):
  name = StringField(required=True, validators=[validate_not_empty()])
  email = StringField(required=True, validators=[
                      validate_required(), validate_email(), validate_not_empty()])
  content = StringField(required=True, validators=[
                        validate_required(), validate_not_empty()])
  id = IntegerField()
  created_at = DateTimeField()

  # messages = {
  #     "name.required": "Invalid name",
  #     "email.required": "Invalid email",
  #     "content.required": "Invalid content",
  #     'required': 'invalid'
  # }
  # pass
