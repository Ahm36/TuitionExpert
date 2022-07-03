from django import forms

from main.models import Course
from .models import Notes, Queries, Student, Task, Video

class StudentForm(forms.ModelForm):


    class Meta:
        model = Student
        fields = ['name','place','phone','email','category','course']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['course'].queryset = Course.objects.none()

            if 'category' in self.data:
                try:
                    category_id = int(self.data.get('category'))
                    self.fields['course'].queryset = Course.objects.filter(category_id=category_id).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['course'].queryset = self.instance.category.course_set.order_by('name')


class NotesForm(forms.ModelForm):


    class Meta:
        model = Notes
        fields =['title','file','description']



class VideoForm(forms.ModelForm):


    class Meta:
        model = Video
        fields =['title','file','description']


class TaskUploadForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['question','task_file','description']


class QueryForm(forms.ModelForm):

    class Meta:
        model = Queries
        fields = ['query',]
       