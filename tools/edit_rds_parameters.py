
from boto import rds

connection = rds.RDSConnection(aws_access_key_id='', aws_secret_access_key='')

par = rds.parametergroup.Parameter(name='max_allowed_packet')
par.apply_type = 'integer'
par.apply_method = 'immediate'
par.type = 'integer'
par.set_value(16777216)

group = connection.modify_parameter_group('max-allowed-packet', parameters=[par])

print group.name

