# untraceables

[![Build Status](https://travis-ci.org/Oefenweb/python-untraceables.svg)](https://travis-ci.org/Oefenweb/python-untraceables)

`python-untraceables` provides some tools to randomize IDs for a given set of tables making them untraceable across environments.

## Requirements

* Python 2.7

## Usage

### get-table-list

Gets a list of tables and columns filtered by one or more include / exclude regexes for a given database:

```sh
bin/randomize-ids get-table-list \
  -d example_com_www \
  -i '^users\.id$' \
  -i '^.*\.user_id$' \
  -i '^.*\..*user_id$' \
  -e '^user_application_x_properties\.x_user_id$' \
;
```

Example output:

```sh
example_com_www	audit_trails	user_id
example_com_www	tickets	assigned_user_id
example_com_www	users	id
```

### get-sql

Gets `SQL` statements to randomize the IDs of a given database and table:

```sh
bin/randomize-ids get-sql \
  -d example_com_www \
  -t users \
  -c id \
;
```

or

```sh
bin/randomize-ids get-sql \
  -d example_com_www \
  -t users \
  -c id \
  --mapping-database untraceables \
  --mapping-table users \
;
```

Example output:

```sql
DROP TABLE IF EXISTS `example_com_www`.`_users`;
CREATE TABLE `example_com_www`.`_users` LIKE `example_com_www`.`users`;
INSERT INTO `example_com_www`.`_users` SELECT `t2`.`mapped_id`, `t1`.`username`, `t1`.`password`, `t1`.`active`, `t1`.`first_name`, `t1`.`last_name`, `t1`.`created`, `t1`.`modified` FROM `example_com_www`.`users` `t1` LEFT JOIN `untraceables`.`users` `t2` ON `t2`.`id` = `t1`.`id`;
DROP TABLE `example_com_www`.`users`;
RENAME TABLE `example_com_www`.`_users` TO `example_com_www`.`users`;
```

### run-sql

Runs `SQL` statements from `STDIN`:

```
echo "INSERT INTO example_com_www (a, b, c) VALUES (1, 2, 3)" | \
  bin/randomize-ids run-sql \
    -d example_com_www \
;
```

or

```
echo "INSERT INTO example_com_www (a, b, c) VALUES (1, 2, 3)" | \
  bin/randomize-ids run-sql \
    -d example_com_www \
    --no-foreign-key-checks \
;
```

### all chained together
 
```sh
bin/randomize-ids get-table-list \
  -d example_com_www \
  -i '^users\.id$' -i '^.*\.user_id$' \
  -i '^.*\..*user_id$' \
  -e '^user_application_x_properties\.x_user_id$' | \
  awk '{print "bin/randomize-ids get-sql" " -d " $1 " -t " $2 " -c " $3 " --mapping-table users;" }' | \
  bash -e -o pipefail | \
  bin/randomize-ids run-sql \
    -d example_com_www \
    --no-foreign-key-checks \
;
```
