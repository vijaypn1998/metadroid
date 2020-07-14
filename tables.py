import peewee
import datetime
database = peewee.MySQLDatabase('database_1', user='metadroid', password='Hashcrack#1',
                         host='18.219.186.156', port=3306)
class BaseModel(peewee.Model):
    class Meta:
        database = database

class Account(BaseModel):
    """
    This schema defines google accounts that can be 
    used in conjunction with the GooglePlayAPI
    """
    email_address = peewee.CharField(primary_key=True)
    password = peewee.CharField()
class Apk(BaseModel):
    """
    This schema stores information regarding apks
    """
    apk_id = peewee.CharField(primary_key=True)
    title = peewee.CharField(null=True)
    creator = peewee.CharField(null=True)
    details_url = peewee.CharField(null=True)
    share_url = peewee.CharField(null=True)
    reviews_url = peewee.CharField(null=True)
    subtitle = peewee.CharField(null=True)
    description_short = peewee.CharField(null=True)
    star_rating = peewee.IntegerField(null=True)
    comment_count = peewee.IntegerField(null=True)
    developer_name = peewee.CharField(null=True)
    app_category = peewee.CharField(null=True)
    content_rating = peewee.IntegerField(null=True)
    installation_size = peewee.IntegerField(null=True)
    developer_email = peewee.CharField(null=True)
    developer_website = peewee.CharField(null=True)
    num_downloads_lower = peewee.IntegerField(null=True)
    num_downloads_upper = peewee.IntegerField(null=True)
    upload_date = peewee.DateField(null=True)
    app_type = peewee.CharField(null=True)
    unstable = peewee.BooleanField(null=True)
    contains_ads = peewee.BooleanField(null=True)
    icon_url = peewee.CharField(null=True)
    feature_graphic = peewee.CharField(null=True)

    #Custom Fields
    is_downloaded = peewee.BooleanField(default=False)
    storage_path = peewee.CharField(null=True)
class ApkFolder(BaseModel):
    """
    This schema defines information regarding parsed
    apk folders
    """
    apk_folder_id = peewee.AutoField(primary_key=True)
    does_exist = peewee.BooleanField()
    apk_folder_path = peewee.CharField()
class Dependency(BaseModel):
    """
    This schema stores information regarding dependencies in the corresponding apk
    """
    apk_id = peewee.ForeignKeyField(Apk, field='apk_id', index=True)
    dependency = peewee.CharField(index=True)
    version=peewee.IntegerField()
    
    class Meta:
        primary_key = peewee.CompositeKey('apk_id', 'dependency')
class Job(BaseModel):
    """
    This schema stores information regarding a metadroid "Job"
    """
    job_id = peewee.AutoField(primary_key=True)
    job_status = peewee.IntegerField()
    apps_per_download_group = peewee.IntegerField(null=True)
    apps_per_app_parse_group = peewee.IntegerField(null=True)
    apps_per_manifest_extract_group = peewee.IntegerField(null=True)
    apps_per_delete_group = peewee.IntegerField(null=True)
    wait_time = peewee.IntegerField(null=True)
    download_type = peewee.IntegerField(null=True)
    app_parse_type = peewee.IntegerField(null=True)
    manifest_extract_type = peewee.IntegerField(null=True)
    email_address = peewee.CharField(null=True)
    password = peewee.CharField(null=True)
    category = peewee.CharField(null=True)
    sub_category = peewee.CharField(null=True)
    total_apps = peewee.IntegerField(null=True)
    download_path = peewee.CharField(null=True)
    manifest_path = peewee.CharField(null=True)
    apk_folder_path = peewee.CharField(null=True)
    offset = peewee.IntegerField(null=True)
    should_delete_apks = peewee.BooleanField(null=True)
    should_download_apks = peewee.BooleanField(null=True)
    should_parse_apks = peewee.BooleanField(null=True)
    should_extract_manifest = peewee.BooleanField(null=True)
    use_accounts_json = peewee.BooleanField(null=True)
    json_data = peewee.CharField(null=True)
    publisher = peewee.CharField(null=True)

    #Custom Fields
    created = peewee.DateTimeField(default=datetime.datetime.now)
    last_updated = peewee.TimestampField()
class Manifest(BaseModel):
    """
    This schema stores information regarding stored apk manifests
    """
    manifest_id = peewee.CharField(primary_key=True)
    does_exist = peewee.BooleanField()
    storage_path = peewee.CharField()
class Permission(BaseModel):
    """
    This schema stores information apk permissions
    """
    apk_id = peewee.ForeignKeyField(Apk, field='apk_id', index=True)
    permission = peewee.CharField(index=True)
    
    class Meta:
        primary_key = peewee.CompositeKey('apk_id', 'permission')
class Screenshot(BaseModel):
    """
    This schema stores information regarding apk screenshots
    """
    screenshot_url = peewee.CharField(primary_key=True)
    apk_id = peewee.ForeignKeyField(Apk, field='apk_id', index=True)
class Version(BaseModel):
    """
    This schema stores information regarding apk versions
    """
    apk_id = peewee.ForeignKeyField(model=Apk, field='apk_id', column_name='apk_id', index=True)
    version = peewee.IntegerField()
    does_exist = peewee.BooleanField(default=False)
    
    class Meta:
        primary_key = peewee.CompositeKey('apk_id', 'version')
def create_tables():
    with database:
        database.create_tables([Account,Apk,ApkFolder,Dependency,Job,Manifest,Permission,Screenshot,Version])
create_tables()
