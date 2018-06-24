def get_codes_subquery(get_rates_request):
    return "WITH originports as\
            (\
              WITH originqualifiedregions AS\
              (\
                WITH RECURSIVE allregions AS\
                (\
                  SELECT slug\
                  FROM regions\
                  WHERE parent_slug = '{0}'\
                  UNION ALL\
                  SELECT singleregion.slug\
                  FROM regions singleregion\
                    JOIN allregions\
                      ON singleregion.parent_slug = allregions.slug\
                )\
                SELECT *\
                FROM allregions\
              )\
              select code from ports where parent_slug in (select * from originqualifiedregions) or parent_slug = '{0}'\
              or code = '{0}'\
            ),\
            destinationports as\
            (\
              WITH originqualifiedregions AS\
              (\
                WITH RECURSIVE allregions AS\
                (\
                  SELECT slug\
                  FROM regions\
                  WHERE parent_slug = '{1}'\
                  UNION ALL\
                  SELECT singleregion.slug\
                  FROM regions singleregion\
                    JOIN allregions\
                      ON singleregion.parent_slug = allregions.slug\
                )\
                SELECT *\
                FROM allregions\
              )\
              select code from ports where parent_slug in (select * from originqualifiedregions) or parent_slug = '{1}'\
              or code = '{1}'\
            )\
            ".format(get_rates_request.origin, get_rates_request.destination)


def get_rates_query(get_rates_request):
    return get_codes_subquery(get_rates_request) + "select day, avg(price) as Average_Price\
    from prices where orig_code IN (select * from originports)\
    and dest_code IN (select * from destinationports)\
    and (day >= '{0}' and day <= '{1}') Group By day Order By day;\
    ".format(get_rates_request.date_from, get_rates_request.date_to)


def get_rates_query_null(get_rates_request):
    return get_codes_subquery(get_rates_request) + "select day, CASE WHEN count(*) > 3 THEN avg(price) else null END as\
        Average_Price\
        from prices where orig_code IN (select * from originports)\
        and dest_code IN (select * from destinationports)\
        and (day >= '{0}' and day <= '{1}') Group By day Order By day;\
        ".format(get_rates_request.date_from, get_rates_request.date_to)
