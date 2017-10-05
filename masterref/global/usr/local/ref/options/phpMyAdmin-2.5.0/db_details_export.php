<?php
/* $Id: db_details_export.php,v 1.13 2003/03/12 15:21:43 garvinhicking Exp $ */
// vim: expandtab sw=4 ts=4 sts=4:


/**
 * Gets some core libraries
 */
$sub_part  = '_export';
require('./db_details_common.php');
$url_query .= '&amp;goto=db_details_export.php';
require('./db_details_db_info.php');

/**
 * Displays the form
 */
?>
<h2>
    <?php echo $strViewDumpDB; ?>
</h2>

<?php
$multi_tables = '';
if ($num_tables > 1) {

    $multi_tables = '<div align="center"><select name="table_select[]" size="6" multiple="multiple">';
    $multi_tables .= "\n";
    
    $i = 0;
    $is_selected = (!empty($selectall) ? ' selected="selected"' : '');
    while ($i < $num_tables) {
        $table   = htmlspecialchars((PMA_MYSQL_INT_VERSION >= 32303) ? $tables[$i]['Name'] : $tables[$i]);
        $multi_tables .= '                <option value="' . $table . '"' . $is_selected . '>' . $table . '</option>' . "\n";
        $i++;
    } // end while
    $multi_tables .= "\n";
    $multi_tables .= '</select></div>';

    $checkall_url = 'db_details_export.php?' 
                  . PMA_generate_common_url($db)
                  . '&amp;goto=db_details_export.php';
    
    $multi_tables .= '<br />
            <a href="' . $checkall_url . '&amp;selectall=1#dumpdb" onclick="setSelectOptions(\'db_dump\', \'table_select[]\', true); return false;">' . $strSelectAll . '</a>
            &nbsp;/&nbsp;
            <a href="' . $checkall_url . '#dumpdb" onclick="setSelectOptions(\'db_dump\', \'table_select[]\', false); return false;">' . $strUnselectAll . '</a>
            <br /><br />';
}  // end if
echo "\n";

$tbl_dump_form_name = 'db_dump';
require('./libraries/display_export.lib.php');

/**
 * Displays the footer
 */
require('./footer.inc.php');
?>
