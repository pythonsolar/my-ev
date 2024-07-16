from django.db import models
from django.contrib import auth
#User = auth.get_user_model()

# class Device(models.Model):
#     name = models.CharField(max_length=255, null=True, blank=True)
#     serial = models.CharField(max_length=255, null=True, blank=True)


class Address(models.Model):
    address_pk = models.PositiveIntegerField(primary_key=True, unique=True, auto_created=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    house_number = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        # abstract = True
        app_label = ''
        db_table = 'address'
        verbose_name_plural = 'addresses'

class ChargingProfile(models.Model):
    charging_profile_pk = models.AutoField(primary_key=True)
    stack_level = models.IntegerField()
    charging_profile_purpose = models.CharField(max_length=255)
    charging_profile_kind = models.CharField(max_length=255)
    recurrency_kind = models.CharField(max_length=255, null=True, blank=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    duration_in_seconds = models.IntegerField(null=True, blank=True)
    start_schedule = models.DateTimeField(null=True, blank=True)
    charging_rate_unit = models.CharField(max_length=255)
    min_charging_rate = models.DecimalField(max_digits=15, decimal_places=1, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.charging_profile_purpose} - {self.charging_profile_kind}"
    
class ChargingSchedulePeriod(models.Model):
    charging_profile = models.ForeignKey(ChargingProfile, on_delete=models.CASCADE)
    start_period_in_seconds = models.IntegerField()
    power_limit = models.DecimalField(max_digits=15, decimal_places=1)
    number_phases = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = (('charging_profile', 'start_period_in_seconds'),)

    def __str__(self):
        return f"Profile {self.charging_profile.charging_profile_pk}, Start {self.start_period_in_seconds}"
    
class ChargeBox(models.Model):
    charge_box_pk = models.AutoField(primary_key=True)
    charge_box_id = models.CharField(max_length=255, unique=True)
    endpoint_address = models.CharField(max_length=255, null=True, blank=True)
    ocpp_protocol = models.CharField(max_length=255, null=True, blank=True)
    registration_status = models.CharField(max_length=255, default='Accepted')
    charge_point_vendor = models.CharField(max_length=255, null=True, blank=True)
    charge_point_model = models.CharField(max_length=255, null=True, blank=True)
    charge_point_serial_number = models.CharField(max_length=255, null=True, blank=True)
    charge_box_serial_number = models.CharField(max_length=255, null=True, blank=True)
    fw_version = models.CharField(max_length=255, null=True, blank=True)
    fw_update_status = models.CharField(max_length=255, null=True, blank=True)
    fw_update_timestamp = models.DateTimeField(null=True, blank=True)
    iccid = models.CharField(max_length=255, null=True, blank=True)
    imsi = models.CharField(max_length=255, null=True, blank=True)
    meter_type = models.CharField(max_length=255, null=True, blank=True)
    meter_serial_number = models.CharField(max_length=255, null=True, blank=True)
    diagnostics_status = models.CharField(max_length=255, null=True, blank=True)
    diagnostics_timestamp = models.DateTimeField(null=True, blank=True)
    last_heartbeat_timestamp = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    location_latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    location_longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)

    address = models.ForeignKey(Address, to_field='address_pk', db_column='address_pk', related_name="charge_boxes", on_delete=models.CASCADE)
    admin_address = models.CharField(max_length=255, null=True, blank=True)
    insert_connector_status_after_transaction_msg = models.BooleanField(default=True)

    class Meta:
        # abstract = True
        unique_together = (('ocpp_protocol', 'endpoint_address'),)
        indexes = [
            models.Index(fields=['ocpp_protocol', 'endpoint_address']),
        ]
        app_label = ''
        db_table = 'charge_box'
        verbose_name_plural = 'charge_boxs'

    def __str__(self):
        return self.charge_box_id
    
class Connector(models.Model):
    connector_pk = models.PositiveIntegerField(primary_key=True, unique=True, auto_created=True)
    charge_box = models.ForeignKey(ChargeBox, to_field='charge_box_id', related_name="connectors", on_delete=models.CASCADE)
    connector_id = models.IntegerField()

    class Meta:
        unique_together = (('charge_box_id', 'connector_id'),)
        app_label = ''
        db_table = 'connector'
        verbose_name_plural = 'connectors'

    def __str__(self):
        return f"Charge Box ID: {self.charge_box_id}, Connector ID: {self.connector_id}"
    
class ConnectorChargingProfile(models.Model):
    connector_pk = models.ForeignKey(Connector, on_delete=models.CASCADE)
    charging_profile_pk = models.ForeignKey(ChargingProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('connector_pk', 'charging_profile_pk'),)
        app_label = ''
        db_table = 'connector_charging_profile'
        verbose_name_plural = 'connector_charging_profiles'

    def __str__(self):
        return f"Connector PK: {self.connector_pk.connector_pk}, Charging Profile PK: {self.charging_profile_pk.charging_profile_pk}"
    
class ConnectorStatus(models.Model):
    connector_pk = models.ForeignKey(Connector, on_delete=models.CASCADE)
    status_timestamp = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    error_code = models.CharField(max_length=255, null=True, blank=True)
    error_info = models.CharField(max_length=255, null=True, blank=True)
    vendor_id = models.CharField(max_length=255, null=True, blank=True)
    vendor_error_code = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['connector_pk']),
            models.Index(fields=['connector_pk', 'status_timestamp']),
        ]
        app_label = ''
        db_table = 'connector_status'
        verbose_name_plural = 'connector_statuses'

    def __str__(self):
        return f"Connector PK: {self.connector_pk.connector_pk}, Status: {self.status}"
    
class OcppTag(models.Model):
    ocpp_tag_pk = models.AutoField(primary_key=True)
    id_tag = models.CharField(max_length=255, unique=True)
    parent_id_tag = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, to_field='id_tag')
    expiry_date = models.DateTimeField(null=True, blank=True)
    max_active_transaction_count = models.IntegerField(default=1)
    note = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['expiry_date']),
            models.Index(fields=['parent_id_tag']),
        ]
        app_label = ''
        db_table = 'ocpp_tag'
        verbose_name_plural = 'ocpp_tags'

    def __str__(self):
        return self.id_tag
    
class SchemaVersion(models.Model):
    installed_rank = models.IntegerField(primary_key=True)
    version = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200)
    type = models.CharField(max_length=20)
    script = models.CharField(max_length=1000)
    checksum = models.IntegerField(null=True, blank=True)
    installed_by = models.CharField(max_length=100)
    installed_on = models.DateTimeField(auto_now_add=True)
    execution_time = models.IntegerField()
    success = models.BooleanField()

    class Meta:
        indexes = [
            models.Index(fields=['success']),
        ]
        app_label = ''
        db_table = 'schema_version'
        verbose_name_plural = 'schema_versions'
    def __str__(self):
        return f"{self.version} - {self.description}"
    
class Settings(models.Model):
    app_id = models.CharField(max_length=40, primary_key=True, unique=True)
    heartbeat_interval_in_seconds = models.IntegerField(null=True, blank=True)
    hours_to_expire = models.IntegerField(null=True, blank=True)
    mail_enabled = models.BooleanField(default=False)
    mail_host = models.CharField(max_length=255, null=True, blank=True)
    mail_username = models.CharField(max_length=255, null=True, blank=True)
    mail_password = models.CharField(max_length=255, null=True, blank=True)
    mail_from = models.CharField(max_length=255, null=True, blank=True)
    mail_protocol = models.CharField(max_length=255, default='smtp')
    mail_port = models.IntegerField(default=25)
    mail_recipients = models.TextField(null=True, blank=True, help_text='comma separated list of email addresses')
    notification_features = models.TextField(null=True, blank=True, help_text='comma separated list')

    class Meta:
        
        app_label = ''
        db_table = 'settings'
        verbose_name_plural = 'settinges'

    def __str__(self):
        return self.app_id
    
class TransactionStart(models.Model):
    transaction_pk = models.AutoField(primary_key=True)
    event_timestamp = models.DateTimeField(auto_now_add=True)
    connector = models.ForeignKey(Connector,to_field='connector_pk', db_column='connector_pk',
                                  related_name="transaction_starts", on_delete=models.CASCADE)
    tag = models.ForeignKey(OcppTag, to_field='id_tag',db_column='id_tag',
                                  related_name="transaction_starts", on_delete=models.CASCADE)
    start_timestamp = models.DateTimeField(null=True, blank=True)
    start_value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['tag_id']),
            models.Index(fields=['connector_id']),
            models.Index(fields=['start_timestamp']),
        ]
        app_label = ''
        db_table = 'transaction_start'
        verbose_name_plural = 'transaction_starts'

    def __str__(self):
        return f"Transaction {self.transaction_pk} - Connector {self.connector_id}"
    
class TransactionStop(models.Model):
    transaction = models.OneToOneField(TransactionStart,to_field='transaction_pk',db_column='transaction_pk',
                                  related_name="transaction_stop", on_delete=models.CASCADE, primary_key=True)
    event_timestamp = models.DateTimeField(auto_now_add=True)
    event_actor = models.CharField(max_length=20, choices=[('station', 'station'), ('manual', 'manual')], null=True, blank=True)
    stop_timestamp = models.DateTimeField(auto_now_add=True)
    stop_value = models.CharField(max_length=255)
    stop_reason = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = (('transaction_pk', 'event_timestamp'),)
        app_label = ''
        db_table = 'transaction_stop'
        verbose_name_plural = 'transaction_stops'

    def __str__(self):
        return f"Transaction {self.transaction_id} - Stop Event"
    
class TransactionStopFailed(models.Model):
    transaction_pk = models.IntegerField(null=True, blank=True)
    event_timestamp = models.DateTimeField(auto_now_add=True)
    event_actor = models.CharField(max_length=20, choices=[('station', 'station'), ('manual', 'manual')], null=True, blank=True)
    stop_timestamp = models.DateTimeField(auto_now_add=True)
    stop_value = models.CharField(max_length=255, null=True, blank=True)
    stop_reason = models.CharField(max_length=255, null=True, blank=True)
    fail_reason = models.TextField(null=True, blank=True)

    class Meta:
        
        app_label = ''
        db_table = 'transaction_stop_failed'
        verbose_name_plural = 'transaction_stops_failed'

    def __str__(self):
        return f"Transaction {self.transaction_pk} - Stop Failed"

class User(models.Model):
    user_pk = models.AutoField(primary_key=True)
    ocpp_tag_pk = models.ForeignKey(OcppTag, null=True, blank=True, on_delete=models.SET_NULL)
    address_pk = models.ForeignKey(Address, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    birth_day = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    e_mail = models.CharField(max_length=255, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['ocpp_tag_pk']),
            models.Index(fields=['address_pk']),
        ]
        app_label = ''
        db_table = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Reservation(models.Model):
    reservation_pk = models.AutoField(primary_key=True)
    connector_pk = models.ForeignKey(Connector, on_delete=models.CASCADE)
    transaction_pk = models.OneToOneField(TransactionStart, null=True, blank=True, on_delete=models.SET_NULL)
    id_tag = models.ForeignKey(OcppTag, to_field='id_tag', on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(null=True, blank=True)
    expiry_datetime = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['id_tag']),
            models.Index(fields=['start_datetime']),
            models.Index(fields=['expiry_datetime']),
            models.Index(fields=['status']),
            models.Index(fields=['connector_pk']),
        ]
        app_label = ''
        db_table = 'reservation'
        verbose_name_plural = 'reservations'

    def __str__(self):
        return f"Reservation {self.reservation_pk} - Status {self.status}"
    

class ConnectorMeterValue(models.Model):
    connector = models.ForeignKey(Connector, to_field='connector_pk', db_column='connector_pk',
                                  related_name="connector_meter_values", on_delete=models.CASCADE, primary_key=True)
    transaction = models.ForeignKey(TransactionStart, to_field='transaction_pk', db_column='transaction_pk',
        related_name="connector_meter_values", null=True, blank=True, on_delete=models.SET_NULL)
    
    value_timestamp = models.DateTimeField(null=True, blank=True)
    value = models.TextField(null=True, blank=True)
    reading_context = models.CharField(max_length=255, null=True, blank=True)
    format = models.CharField(max_length=255, null=True, blank=True)
    measurand = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    unit = models.CharField(max_length=255, null=True, blank=True)
    phase = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
       

        app_label = ''
        db_table = 'connector_meter_value'
        verbose_name_plural = 'connector_meter_values'

        unique_together = (('connector_pk', 'transaction_pk'),)

    def __str__(self):
        return f"Connector PK: {self.connector_id}, Timestamp: {self.value_timestamp}"


class ConnectorStatus(models.Model):
    connector_pk = models.IntegerField(null=False)
    status_timestamp = models.DateTimeField(default=None, null=True)
    status = models.CharField(max_length=255, default=None, null=True)
    error_code = models.CharField(max_length=255, default=None, null=True)
    error_info = models.CharField(max_length=255, default=None, null=True)
    vendor_id = models.CharField(max_length=255, default=None, null=True)
    vendor_error_code = models.CharField(max_length=255,default=None, null=True)

    class Meta:
        

        app_label = ''
        db_table = 'connector_status'
        verbose_name_plural = 'connector_statuses'

