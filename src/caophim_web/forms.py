from django.forms import HiddenInput, ModelForm, Textarea, ValidationError

from .models import Post


class RequiredFieldsModelForm(ModelForm):
    required_fields = tuple()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required_fields:
            self.fields[field].required = True


class CreateThreadForm(RequiredFieldsModelForm):
    class Meta:
        model = Post
        fields = ("board", "subject", "comment", "pic")
        required_fields = ("board", "pic")
        widgets = {
            "board": HiddenInput(),
            "comment": Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if not (cleaned_data.get("subject") or cleaned_data.get("comment")):
            raise ValidationError("Missing both subject and comment.")


class CreateReplyForm(RequiredFieldsModelForm):
    class Meta:
        model = Post
        fields = ("parent_thread", "comment", "pic")
        required_fields = ("parent_thread",)
        widgets = {
            "parent_thread": HiddenInput(),
            "comment": Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if not (cleaned_data.get("comment") or cleaned_data.get("pic")):
            raise ValidationError("Missing both comment and pic.")
