# untraceables

[![Build Status](https://travis-ci.org/Oefenweb/python-untraceables.svg)](https://travis-ci.org/Oefenweb/python-untraceables)

`python-untraceables` provides some tools to randomize IDs for a given set of tables making them untraceable across environments.

## Requirements

* Python 2.7
* Python 3.5
* Python 3.6

## Usage

### Setup

#### Untraceables user, database and mapping table

Create a `untraceables` user with sufficient permissions.

```sql
CREATE USER 'untraceables'@'localhost' IDENTIFIED BY 'mmRXHqnc3zSshYjxSv8n';
CREATE DATABASE untraceables;
GRANT SELECT ON untraceables . * TO 'untraceables'@'localhost';
```

```sql
GRANT ALL PRIVILEGES ON example_com_www . * TO 'untraceables'@'localhost';
FLUSH PRIVILEGES;
```

Let's say we want to randomize IDs for our `users` table.

```sql
USE `untraceables`;
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(10) unsigned NOT NULL,
  `mapped_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mapped_id` (`mapped_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

#### Configuration

Create the necessary configuration file.

```sh
# cat /etc/untraceables.cfg
[main]
# Database host
host = localhost

# Database user, read-only on untraceables database, write on databases that need randomized IDs
user = untraceables
password = mmRXHqnc3zSshYjxSv8n
```

#### Generate mapping table data

Generate a file containing the full unsinged integer range.

```sh
# 2^32 - 1 = 4294967295
seq -f '%.0f' 0 4294967295 > unsinged-int;
```

Shuffle the file. **Note** that this may need a lot om RAM. `unsinged-int` is about `40G`, RAM usage for the shuffle was `107G`.

```sh
shuf < unsinged-int > unsinged-int.shuf;
```

Combine the ordered unsinged integer range with the shuffled one. Also split the output in pieces of `10^6` IDs.

```sh
paste unsinged-int unsinged-int.shuf | split --numeric-suffixes -l 1000000 - unsinged-int.csv-;
```

Compress all pieces

```sh
ls unsinged-int.csv-* | parallel -j 12 'gzip {}';
```

#### Load mapping table data

Load the first piece of compressed data into MySQL.

In one terminal

```sh
mkfifo --mode=0600 users.csv;
gunzip < unsinged-int.csv-00.gz > users.csv;
```

In another

```sh
mysqlimport --fields-terminated-by='\t' --ignore-lines=0 --local untraceables users.csv;
```

This loads `unsinged-int.csv-00.gz` into `untraceables`.`users`.

### Commands

#### get-include-from-mydumper-backup

Generates a list of include regexes, from a given mydymper backup, to be used as imput for `get-table-list`.

```sh
bin/randomize-ids get-include-from-mydumper-backup \
  -d example_com_www \
  -p ~/backups/latest/ \
  -i '^users\.id$' \
  -i '^.*\.user_id$' \
  -i '^.*\..*user_id$' \
  > /tmp/include-from \
;
```

#### get-table-list

Gets a list of tables and columns filtered by one or more include / exclude regexes for a given database.

```sh
bin/randomize-ids get-table-list \
  -d example_com_www \
  -i '^users\.id$' \
  -i '^.*\.user_id$' \
  -i '^.*\..*user_id$' \
  -e '^user_application_x_properties\.x_user_id$' \
;
```

or

```sh
bin/randomize-ids get-table-list -d example_com_www \
  --include-from /tmp/include-from \
  -e '^user_application_x_properties\.x_user_id$' \
;
```

Example output.

```sh
example_com_www	audit_trails	user_id
example_com_www	tickets	assigned_user_id
example_com_www	users	id
```

#### get-sql

Gets `SQL` statements to randomize the IDs of a given database and table.

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

Example output.

```sql
DROP TABLE IF EXISTS `example_com_www`.`_users`;
CREATE TABLE `example_com_www`.`_users` LIKE `example_com_www`.`users`;
INSERT INTO `example_com_www`.`_users` SELECT `t2`.`mapped_id`, `t1`.`username`, `t1`.`password`, `t1`.`active`, `t1`.`first_name`, `t1`.`last_name`, `t1`.`created`, `t1`.`modified` FROM `example_com_www`.`users` `t1` LEFT JOIN `untraceables`.`users` `t2` ON `t2`.`id` = `t1`.`id`;
DROP TABLE `example_com_www`.`users`;
RENAME TABLE `example_com_www`.`_users` TO `example_com_www`.`users`;
```

#### run-sql

Runs `SQL` statements from `STDIN`.

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

#### All chained together
 
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
