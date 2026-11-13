from django.db import transaction
from django.db.models import FileField


def delete_on_model_delete(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if isinstance(field, FileField):
            file = getattr(instance, field.name)
            if file and file.storage.exists(file.name):
                transaction.on_commit(lambda f=file: f.delete(save=False))


def delete_old_file(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    for field in instance._meta.fields:
        if isinstance(field, FileField):
            old_file = getattr(old_instance, field.name)
            new_file = getattr(instance, field.name)

            if old_file and old_file != new_file:
                old_name = old_file.name
                storage = old_file.storage

                def cleanup(f_name=old_name, st=storage, inst=instance, fld=field.name):
                    current_file = getattr(inst, fld)
                    if (not current_file or current_file.name != f_name) and st.exists(f_name):
                        st.delete(f_name)

                transaction.on_commit(cleanup)
