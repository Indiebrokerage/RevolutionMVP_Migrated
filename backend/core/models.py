# RevolutionMVP_Django/core/models.py

from django.db import models

# Model for mail_activity_log
class MailActivityLog(models.Model):
    id = models.AutoField(primary_key=True)
    from_id = models.IntegerField()
    from_mail = models.TextField(null=True, blank=True)
    from_type = models.IntegerField(help_text='1 : send from contacts , 2 : send from inquiries')
    from_name = models.CharField(max_length=255, null=True, blank=True)
    to_id = models.IntegerField()
    to_mail = models.TextField(null=True, blank=True)
    to_type = models.IntegerField(help_text='1 : send from contacts , 2 : send from inquiries')
    to_name = models.CharField(max_length=255, null=True, blank=True)
    subject = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    send_at = models.DateTimeField(null=True, blank=True)
    attach_file = models.TextField(null=True, blank=True)
    status_type = models.IntegerField(default=1, help_text='1:sended , 2:reply')
    message_id = models.CharField(max_length=255, null=True, blank=True)
    parent_message_id = models.CharField(max_length=255, null=True, blank=True)
    parent_id = models.CharField(max_length=255, null=True, blank=True)
    send_status = models.IntegerField(default=0, help_text='1 : send success , 0 : send false')
    create_at = models.DateTimeField(null=True, blank=True)
    create_ip = models.IntegerField(null=True, blank=True)
    is_readed = models.IntegerField(default=0, null=True, blank=True, help_text='0: mail not read , 1 : mail had readed ')

    class Meta:
        db_table = 'mail_activity_log'

# Model for mail_signature
class MailSignature(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    status = models.IntegerField(null=True, blank=True, help_text='1 : use signature , 0 : not use signature')
    signature = models.TextField(null=True, blank=True)
    update_at = models.DateTimeField(null=True, blank=True)
    create_at = models.DateTimeField(null=True, blank=True)
    create_ip = models.IntegerField(null=True, blank=True)
    update_ip = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'mail_signature'

# Model for route_matrix (assuming it's a control table)
class RouteMatrix(models.Model):
    id = models.AutoField(primary_key=True)
    route_name = models.CharField(max_length=255)
    guest = models.IntegerField()
    user = models.IntegerField()
    vendor = models.IntegerField()
    agent = models.IntegerField()
    system_admin = models.IntegerField()
    super_admin = models.IntegerField()

    class Meta:
        db_table = 'route_matrix'

# Model for dat_property_import (partial definition based on ALTER TABLE)
class DatPropertyImport(models.Model):
    # Assuming existing fields, adding status_rest
    status_rest = models.TextField(null=True, blank=True, help_text='Status of Property in Matrix Stite')

    class Meta:
        db_table = 'dat_property_import'
        managed = False # This table's full schema is not defined here, only altered

# Model for dat_property (partial definition based on ALTER TABLE)
class DatProperty(models.Model):
    # Assuming existing fields, adding status_rest, open_house_from, open_house_to, status_manual
    status_rest = models.TextField(null=True, blank=True, help_text='Status of Property in Matrix Stite')
    open_house_from = models.DateTimeField(null=True, blank=True)
    open_house_to = models.DateTimeField(null=True, blank=True)
    status_manual = models.IntegerField(default=0, null=True, blank=True, help_text='status set by user . 0 : none , 1: opend house,...')

    class Meta:
        db_table = 'dat_property'
        managed = False # This table's full schema is not defined here, only altered

# Model for ctr_property_column
class CtrPropertyColumn(models.Model):
    column_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ctr_property_column'
        managed = False # This table's full schema is not defined here, only altered

# Model for lnk_column_map
class LnkColumnMap(models.Model):
    feed_column_id = models.IntegerField()
    column_name = models.CharField(max_length=255)
    additional_logic = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'lnk_column_map'
        managed = False # This table's full schema is not defined here, only altered

# Model for contacts_searches
class ContactsSearches(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.IntegerField()
    region = models.CharField(max_length=255, null=True, blank=True)
    date_login_from = models.DateTimeField(null=True, blank=True)
    date_login_to = models.DateTimeField(null=True, blank=True)
    login_count = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    user_created = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    user_updated = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'contacts_searches'

# Model for dat_awards
class DatAwards(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    created_id = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'dat_awards'

# Model for dat_user_attribute (partial definition based on ALTER TABLE)
class DatUserAttribute(models.Model):
    # Assuming existing fields, adding cover_image, googlemap_lt, googlemap_ln
    cover_image = models.TextField(null=True, blank=True)
    googlemap_lt = models.CharField(max_length=255, null=True, blank=True)
    googlemap_ln = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'dat_user_attribute'
        managed = False # This table's full schema is not defined here, only altered

# Model for dat_projects
class DatProjects(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    date_created = models.DateField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    number_view = models.IntegerField(null=True, blank=True)
    zip = models.TextField(null=True, blank=True)
    created_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    update_id = models.IntegerField(null=True, blank=True)
    update_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'dat_projects'

# Model for dat_projects_images
class DatProjectsImages(models.Model):
    id = models.AutoField(primary_key=True)
    projects_id = models.IntegerField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    created_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    update_id = models.IntegerField(null=True, blank=True)
    update_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'dat_projects_images'

# Model for dat_projects_videos
class DatProjectsVideos(models.Model):
    id = models.AutoField(primary_key=True)
    projects_id = models.IntegerField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    video_url = models.TextField(null=True, blank=True)
    created_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    update_id = models.IntegerField(null=True, blank=True)
    update_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'dat_projects_videos'

# Model for ctr_table_type
class CtrTableType(models.Model):
    table_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ctr_table_type'
        managed = False # This table's full schema is not defined here, only altered

# Model for ctr_tables
class CtrTables(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    parent_id = models.IntegerField(null=True, blank=True)
    type_id = models.IntegerField(null=True, blank=True)
    client_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'ctr_tables'
        managed = False # This table's full schema is not defined here, only altered

# Model for user_bookmark_project
class UserBookmarkProject(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    project_id = models.IntegerField()
    book_mark_flash = models.SmallIntegerField(default=0, help_text='0 is unsaved, 1 is saved')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user_bookmark_project'

# Model for vendor_rating
class VendorRating(models.Model):
    id = models.AutoField(primary_key=True)
    user_reviewed_id = models.IntegerField()
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    appreciation = models.TextField()
    score = models.IntegerField()
    user_created = models.IntegerField()
    user_updated = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'vendor_rating'

# Model for comment_review
class CommentReview(models.Model):
    id = models.AutoField(primary_key=True)
    id_review = models.IntegerField(null=True, blank=True)
    user_comment = models.IntegerField(null=True, blank=True)
    comment = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'comment_review'

# Model for dat_contacts (partial definition based on ALTER TABLE)
class DatContacts(models.Model):
    # Assuming existing fields, adding is_hide_display
    is_hide_display = models.IntegerField(default=1, null=True, blank=True, help_text='show or hide question in list vendor detail . 0 : show , 1: hide')

    class Meta:
        db_table = 'dat_contacts'
        managed = False # This table's full schema is not defined here, only altered

# Model for dat_like_reviews
class DatLikeReviews(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    vendor_rating_id = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True, help_text='0 : like , 1: unlike')
    created_at = models.DateTimeField(auto_now_add=True)
    created_id = models.IntegerField()
    update_at = models.DateTimeField(auto_now=True)
    update_id = models.IntegerField()

    class Meta:
        db_table = 'dat_like_reviews'

# Sentinel Models (from migration_cartalyst_sentinel.php)

class Activation(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(db_index=True)
    code = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'activations'

class Persistence(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(db_index=True)
    code = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'persistences'

class Reminder(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(db_index=True)
    code = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reminders'

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    permissions = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'roles'

class RoleUser(models.Model):
    user_id = models.IntegerField()
    role_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'role_users'
        unique_together = (('user_id', 'role_id'),)

class Throttle(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True, db_index=True)
    type = models.CharField(max_length=255)
    ip = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'throttle'

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    permissions = models.TextField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'


