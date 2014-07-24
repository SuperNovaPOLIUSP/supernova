import autocomplete_light
from models import Course

class CourseAutoComplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^coursecode', ]

autocomplete_light.register(Course, CourseAutoComplete)
