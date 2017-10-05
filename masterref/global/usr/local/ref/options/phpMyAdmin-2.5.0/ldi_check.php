<?php
/* $Id: ldi_check.php,v 1.26 2003/03/21 11:58:49 nijel Exp $ */
// vim: expandtab sw=4 ts=4 sts=4:


/**
 * This file checks and builds the sql-string for
 * LOAD DATA INFILE 'file_name.txt' [REPLACE | IGNORE] INTO TABLE table_name
 *    [FIELDS
 *        [TERMINATED BY '\t']
 *        [OPTIONALLY] ENCLOSED BY "]
 *        [ESCAPED BY '\\' ]]
 *    [LINES TERMINATED BY '\n']
 *    [(column_name,...)]
 */


/**
 * Gets some core scripts
 */
require('./libraries/grab_globals.lib.php');
require('./libraries/common.lib.php');


/**
 * The form used to define the query has been submitted -> do the work
 */
if (isset($btnLDI) && ($textfile != 'none')) {
    if (!isset($replace)) {
        $replace = '';
    }

    error_reporting(E_ALL);
    chmod($textfile, 0644);

    // Kanji encoding convert appended by Y.Kawada
    if (function_exists('PMA_kanji_file_conv')) {
        $textfile         = PMA_kanji_file_conv($textfile, $knjenc, isset($xkana) ? $xkana : '');
    }

    // Convert the file's charset if necessary
    if ($cfg['AllowAnywhereRecoding'] && $allow_recoding
        && isset($charset_of_file) && $charset_of_file != $charset) {
        $textfile         = PMA_convert_file($charset_of_file, $convcharset, $textfile);
    }

    // Formats the data posted to this script
    $textfile             = PMA_sqlAddslashes($textfile);
    $enclosed             = PMA_sqlAddslashes($enclosed);
    $escaped              = PMA_sqlAddslashes($escaped);
    $column_name          = PMA_sqlAddslashes($column_name);

    // (try to) make sure the file is readable:
    chmod($textfile, 0777);

    // Builds the query
    $sql_query     =  'LOAD DATA';

    // for versions before 3.23.49, we use the LOCAL keyword, because
    // there was a version (cannot find which one, and it does not work
    // with 3.23.38) where the user can LOAD, even if the user does not
    // have FILE priv, and even if the file is on the server
    // (which is the present case)
    //
    // we could also code our own loader, but LOAD DATA INFILE is optimized
    // for speed

    if (PMA_MYSQL_INT_VERSION < 32349) {
        $sql_query     .= ' LOCAL';
    }

    if (PMA_MYSQL_INT_VERSION > 40003) {
        $tmp_query  = "SHOW VARIABLES LIKE 'local\\_infile'";
        $result = PMA_mysql_query($tmp_query);
        if ($result != FALSE && mysql_num_rows($result) > 0) {
            $tmp = PMA_mysql_fetch_row($result);
            if ($tmp[1] == 'ON') {
                $sql_query     .= ' LOCAL';
            }
        }
        mysql_free_result($result);
    }

    $sql_query     .= ' INFILE \'' . $textfile . '\'';
    if (!empty($replace)) {
        $sql_query .= ' ' . $replace;
    }
    $sql_query     .= ' INTO TABLE ' . PMA_backquote($into_table);
    if (isset($field_terminater)) {
        $sql_query .= ' FIELDS TERMINATED BY \'' . $field_terminater . '\'';
    }
    if (isset($enclose_option) && strlen($enclose_option) > 0) {
        $sql_query .= ' OPTIONALLY';
    }
    if (strlen($enclosed) > 0) {
        $sql_query .= ' ENCLOSED BY \'' . $enclosed . '\'';
    }
    if (strlen($escaped) > 0) {
        $sql_query .= ' ESCAPED BY \'' . $escaped . '\'';
    }
    if (strlen($line_terminator) > 0){
        $sql_query .= ' LINES TERMINATED BY \'' . $line_terminator . '\'';
    }
    if (strlen($column_name) > 0) {
        if (PMA_MYSQL_INT_VERSION >= 32306) {
            $sql_query .= ' (';
            $tmp   = split(',( ?)', $column_name);
            for ($i = 0; $i < count($tmp); $i++) {
                if ($i > 0) {
                    $sql_query .= ', ';
                }
                $sql_query     .= PMA_backquote(trim($tmp[$i]));
            } // end for
            $sql_query .= ')';
        } else {
            $sql_query .= ' (' . $column_name . ')';
        }
    }

    // We could rename the ldi* scripts to tbl_properties_ldi* to improve
    // consistency with the other sub-pages.
    //
    // The $goto in ldi_table.php is set to tbl_properties.php but maybe
    // if would be better to Browse the latest inserted data.
    include('./sql.php');
}


/**
 * The form used to define the query hasn't been yet submitted -> loads it
 */
else {
    include('./ldi_table.php');
}
?>
