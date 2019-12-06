from django.forms import ModelForm

from caoweb.models import Post


class ForceRequiredFieldsModelForm(ModelForm):
    # make sure all listed fields are required regardless of what
    # their model's `blank` option is:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.fields:
            self.fields[field].required = True


class CreateThreadForm(ForceRequiredFieldsModelForm):
    class Meta:
        model = Post
        fields = ("board", "subject", "comment")


class CreateReplyForm(ForceRequiredFieldsModelForm):
    class Meta:
        model = Post
        fields = ("parent_thread", "comment")
