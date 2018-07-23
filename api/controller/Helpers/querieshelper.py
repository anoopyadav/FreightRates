def get_codes_subquery(request):
    return "WITH originports as\
            (\
              WITH originqualifiedregions AS\
              (\
                WITH RECURSIVE allregions AS\
                (\
                  SELECT slug\
                  FROM regions\
                  WHERE parent_slug = lower('{0}')\
                  UNION ALL\
                  SELECT singleregion.slug\
                  FROM regions singleregion\
                    JOIN allregions\
                      ON singleregion.parent_slug = allregions.slug\
                )\
                SELECT *\
                FROM allregions\
              )\
              select code from ports where parent_slug in \
              (select * from originqualifiedregions) or \
               parent_slug = lower('{0}') or code = upper('{0}')\
            ),\
            destinationports as\
            (\
              WITH originqualifiedregions AS\
              (\
                WITH RECURSIVE allregions AS\
                (\
                  SELECT slug\
                  FROM regions\
                  WHERE parent_slug = lower('{1}')\
                  UNION ALL\
                  SELECT singleregion.slug\
                  FROM regions singleregion\
                    JOIN allregions\
                      ON singleregion.parent_slug = allregions.slug\
                )\
                SELECT *\
                FROM allregions\
              )\
              select code from ports where parent_slug in \
              (select * from originqualifiedregions) or \
               parent_slug = lower('{1}') or code = upper('{1}')\
            )\
            ".format(request.origin_code, request.destination_code)


def get_rates_query(request):
    return get_codes_subquery(request) + \
           "select day, avg(price) as Average_Price\
            from prices where orig_code IN (select * from originports)\
            and dest_code IN (select * from destinationports)\
            and (day >= '{0}' and day <= '{1}') Group By day Order By day;\
            ".format(request.date_from, request.date_to)


def get_rates_query_null(request):
    return get_codes_subquery(request) + \
           "select day, CASE WHEN count(*) > 2 THEN avg(price) else null END as\
            Average_Price\
            from prices where orig_code IN (select * from originports)\
            and dest_code IN (select * from destinationports)\
            and (day >= '{0}' and day <= '{1}') Group By day Order By day;\
            ".format(request.date_from, request.date_to)


def post_rates_query(request):
    return "insert into  prices (orig_code, dest_code, price, day)\
            SELECT '{0}','{1}', {2}, p.day from\
              (\
                select CURRENT_DATE + i as day\
                  from generate_series(date '{3}'- CURRENT_DATE,\
                 date '{4}' - CURRENT_DATE ) i\
              ) p\
            ".format(request.origin_code, request.destination_code,
                     request.price, request.date_from, request.date_to)


def check_ports_query(request):
    return "select count(*) from ports where code IN ('{0}', '{1}')".format(
        request.origin_code, request.destination_code)
