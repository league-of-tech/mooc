from wtforms import StringField, TextAreaField
from wtforms.fields import Field
from wtforms.widgets import TextInput
from wtforms.validators import InputRequired, Length
from wtforms.validators import ValidationError
from flask.ext.babel import lazy_gettext as _
from flask.ext.wtf import Form
from flask.ext.login import current_user


class TagsField(Field):
    """Add a custom Field class.

    This field is designed for tags.
    It will get tags' object according to data in *form_data*.

    :param tag_model: The model of Tag.
    :param label: Label of this field.
    :param validators: Decide validators for this field.
    :param sep: How to seperate tags. Blank by default.
    """
    widget = TextInput()

    def __init__(self, tag_model, label='', validators=None, **kwargs):
        super(TagsField, self).__init__(label, validators, **kwargs)
        self.tag_model = tag_model
        self.sep = kwargs.pop('sep', u' ')

    def _value(self):
        if self.data:
            return self.sep.join([tag.tag for tag in self.data])
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = []
            form_data = valuelist[0].split(self.sep)
            for tag in form_data:
                if not tag.strip():
                    continue
                q_tag = self.tag_model.query.filter_by(tag=tag).first()

                if not q_tag:
                    q_tag = self.tag_model(tag=tag)
                self.data.append(q_tag)
        else:
            self.data = []
            self.data = list(self._remove_duplicates(self.data))

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive,
        but case preserving manner"""
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item


class FeedbackForm(Form):
    title = StringField(
        label=_('Title'),
        validators=[
            InputRequired(),
            Length(max=20),
        ],
    )
    contact = StringField(
        label=_('Contact(Email/QQ)'),
    )
    feedback = TextAreaField(
        label=_('Feedback'),
        validators=[
            InputRequired(),
        ]
    )

    def validate_contact(form, filed):
        if current_user.is_anonymous():
            if len(filed.data) < 1:
                raise ValidationError(unicode(_('This field is required.')))
