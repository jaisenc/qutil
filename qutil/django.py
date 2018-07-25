def df_to_django_model(df):
    for col, type_ in df.dtypes.iteritems():
        if type_ == 'int64':
            dj_type = 'models.BigIntegerField(null=True,black=True)'
        elif type_ == 'object':
            dj_type = 'models.CharField(max_length=200, null=True, blank=False)'
        elif type_ == 'float':
            dj_type = 'models.FloatField(null=True, blank=False)'
        elif type_ == 'datetime64[ns]':
            dj_type = 'models.DateTimeField(null=True, blank=False)'
        else:
            raise ValueError('{} {} not implementy'.format(type_, col))
        print('{} = {}'.format(col, dj_type))

