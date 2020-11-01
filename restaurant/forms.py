from functools import partial
from operator import attrgetter

from django import forms
from django.forms import ModelChoiceField, ModelMultipleChoiceField, CheckboxSelectMultiple
from django.forms.models import ModelChoiceIterator

from restaurant import models
from restaurant.utils import grouped


class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __init__(self, field, group_by):
        self.group_by = group_by
        super().__init__(field)

    def __iter__(self):
        if self.field.empty_label is not None:
            yield "", self.field.empty_label
        queryset = self.queryset
        # Can't use iterator() when queryset uses prefetch_related()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        for group, objs in grouped(queryset, self.group_by).items():
            yield group, list(map(self.choice, objs))


class GroupedModelChoiceMixin:
    def __init__(self, *args, group_by, **kwargs):
        if isinstance(group_by, str):
            group_by = attrgetter(group_by)
        elif not callable(group_by):
            raise TypeError('group_by must either be a str or a callable accepting a single argument')
        self.iterator = partial(GroupedModelChoiceIterator, group_by=group_by)
        super().__init__(*args, **kwargs)


class GroupedModelChoiceField(GroupedModelChoiceMixin, ModelChoiceField):
    """Like ModelChoiceField but groups options"""
    pass


class GroupedModelMultipleChoiceField(GroupedModelChoiceMixin, ModelMultipleChoiceField):
    """Like ModelMultipleChoiceField but groups options"""
    pass


class IndexForm(forms.Form):
    dishes = GroupedModelMultipleChoiceField(queryset=models.Dish.objects.all().select_related("category"),
                                             group_by="category", widget=CheckboxSelectMultiple)


class CreateDishForm(forms.ModelForm):
    class Meta:
        model = models.Dish
        fields = ["name", "nutritional_value", "price", "image", "category", "allergens"]
