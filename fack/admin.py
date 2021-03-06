from __future__ import absolute_import
from django.conf import settings
from django.contrib import admin
from .models import Question, Topic
            
class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'sort_order', 'created_by', 'created_on',
                    'updated_by', 'updated_on', 'status']
    list_editable = ['sort_order', 'status']
    if "redactormedia" in settings.INSTALLED_APPS and getattr(settings, "USE_REDACTOR_FACK", False):
        from redactormedia.widgets import RedactorWithMediaEditor, AdminRedactorWithMediaEditor
        from django.db import models

        formfield_overrides = {
            models.TextField: {'widget': AdminRedactorWithMediaEditor},
        }
        
    def save_model(self, request, obj, form, change): 
        '''
        Update created-by / modified-by fields.
        
        The date fields are upadated at the model layer, but that's not got
        access to the user.
        '''
        # If the object's new update the created_by field.
        if not change:
            obj.created_by = request.user
        
        # Either way update the updated_by field.
        obj.updated_by = request.user

        # Let the superclass do the final saving.
        return super(QuestionAdmin, self).save_model(request, obj, form, change)
        
admin.site.register(Question, QuestionAdmin)
admin.site.register(Topic, TopicAdmin)
