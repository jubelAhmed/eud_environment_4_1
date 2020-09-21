from django.db import models
import simplejson as json
from django.conf import settings
from datetime import datetime
import time

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M:%S')
        return json.JSONEncoder.default(self, obj)

class JSONDecoder(json.JSONDecoder):
    def decode(self, json_string):
        json_data = json.loads(json_string)
        for key in json_data.keys():
            try:
                json_data[key] = datetime.fromtimestamp(time.mktime(time.strptime(json_data[key], "%Y-%m-%d %H:%M:%S")))
            except TypeError:
                # It's not a datetime/time object
                pass
        return json_data

class JSONField(models.TextField):
    def _dumps(self, data):
        return JSONEncoder().encode(data)

    def _loads(self, str):
        return JSONDecoder().decode(str)

    def db_type(self):
        return 'text'

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        return self._dumps(value)

    def contribute_to_class(self, cls, name):
        self.class_name = cls
        super(JSONField, self).contribute_to_class(cls, name)
        models.signals.post_init.connect(self.post_init)

        def get_json(model_instance):
            return self._dumps(getattr(model_instance, self.attname, None))
        setattr(cls, 'get_%s_json' % self.name, get_json)

        def set_json(model_instance, json):
            return setattr(model_instance, self.attname, self._loads(json))
        setattr(cls, 'set_%s_json' % self.name, set_json)

    def post_init(self, **kwargs):
        if 'sender' in kwargs and 'instance' in kwargs:
            if kwargs['sender'] == self.class_name and hasattr(kwargs['instance'], self.attname):
                value = self.value_from_object(kwargs['instance'])
                if (value):
                    setattr(kwargs['instance'], self.attname, self._loads(value))
                else:
                    setattr(kwargs['instance'], self.attname, None)

class JsonModel(models.Model):
    title = models.CharField(max_length=250,null=True, blank=True)
    data = JSONField(null=True, blank=True)

    class Meta:
            verbose_name_plural = 'LiveJsonData'

    def __str__(self):
        return self.title

# data = {'pets': None, 'children': ['Benjamin', 'Clare', 'Joshua'], 'some_date': datetime(2010, 02, 01)}
# # Test decode / encode
# decode = JSONEncoder().encode(data)
# encode = JSONDecoder().decode(decode)

# # Save model
# sample = SampleModel(first_name='Patrick', last_name='Altman')
# sample.data = data
# sample.save()