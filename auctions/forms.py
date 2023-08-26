from django.forms import ModelForm, ModelChoiceField
from auctions.models import Listing, Category, Comment

class ListingForm(ModelForm):
    category = ModelChoiceField(queryset=Category.objects, empty_label=None)
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "imageUrl", "category"]

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)

        #     for field_name, field in self.fields.items():
        #         if not self.fields[field_name].blank:
        #             field.required = True


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]