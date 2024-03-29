<?php
/* $Id: english-utf-8.inc.php,v 1.93 2003/04/25 15:54:12 nijel Exp $ */

$charset = 'utf-8';
$allow_recoding = TRUE;
$text_dir = 'ltr'; // ('ltr' for left to right, 'rtl' for right to left)
$left_font_family = 'verdana, arial, helvetica, geneva, sans-serif';
$right_font_family = 'arial, helvetica, geneva, sans-serif';
$number_thousands_separator = ',';
$number_decimal_separator = '.';
// shortcuts for Byte, Kilo, Mega, Giga, Tera, Peta, Exa
$byteUnits = array('Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB');

$day_of_week = array('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat');
$month = array('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
// See http://www.php.net/manual/en/function.strftime.php to define the
// variable below
$datefmt = '%B %d, %Y at %I:%M %p';
$timespanfmt = '%s days, %s hours, %s minutes and %s seconds';

$strAPrimaryKey = 'A primary key has been added on %s';
$strAbortedClients = 'Aborted';
$strAbsolutePathToDocSqlDir = 'Please enter the absolute path on webserver to docSQL directory';
$strAccessDenied = 'Access denied';
$strAction = 'Action';
$strAddDeleteColumn = 'Add/Delete Field Columns';
$strAddDeleteRow = 'Add/Delete Criteria Row';
$strAddNewField = 'Add new field';
$strAddPriv = 'Add a new Privilege';
$strAddPrivMessage = 'You have added a new privilege.';
$strAddPrivilegesOnDb = 'Add privileges on the following database';
$strAddPrivilegesOnTbl = 'Add privileges on the following table';
$strAddSearchConditions = 'Add search conditions (body of the "where" clause):';
$strAddToIndex = 'Add to index &nbsp;%s&nbsp;column(s)';
$strAddUser = 'Add a new User';
$strAddUserMessage = 'You have added a new user.';
$strAddedColumnComment = 'Added comment for column';
$strAddedColumnRelation = 'Added relation for column';
$strAdministration = 'Administration';
$strAffectedRows = 'Affected rows:';
$strAfter = 'After %s';
$strAfterInsertBack = 'Go back to previous page';
$strAfterInsertNewInsert = 'Insert another new row';
$strAll = 'All';
$strAllTableSameWidth = 'display all Tables with same width?';
$strAlterOrderBy = 'Alter table order by';
$strAnIndex = 'An index has been added on %s';
$strAnalyzeTable = 'Analyze table';
$strAnd = 'And';
$strAny = 'Any';
$strAnyColumn = 'Any Column';
$strAnyDatabase = 'Any database';
$strAnyHost = 'Any host';
$strAnyTable = 'Any table';
$strAnyUser = 'Any user';
$strAscending = 'Ascending';
$strAtBeginningOfTable = 'At Beginning of Table';
$strAtEndOfTable = 'At End of Table';
$strAttr = 'Attributes';
$strAutodetect = 'Autodetect';
$strAutomaticLayout = 'Automatic layout';

$strBack = 'Back';
$strBeginCut = 'BEGIN CUT';
$strBeginRaw = 'BEGIN RAW';
$strBinary = 'Binary';
$strBinaryDoNotEdit = 'Binary - do not edit';
$strBookmarkDeleted = 'The bookmark has been deleted.';
$strBookmarkLabel = 'Label';
$strBookmarkQuery = 'Bookmarked SQL-query';
$strBookmarkThis = 'Bookmark this SQL-query';
$strBookmarkView = 'View only';
$strBrowse = 'Browse';
$strBzError = 'phpMyAdmin was unable to compress the dump because of a broken Bz2 extension in this php version. It is strongly recommended to set the <code>$cfg[\'BZipDump\']</code> directive in your phpMyAdmin configuration file to <code>FALSE</code>. If you want to use the Bz2 compression features, you should upgrade to a later php version. See php bug report %s for details.';
$strBzip = '"bzipped"';

$strCSVOptions = 'CSV options';
$strCannotLogin = 'Cannot login to MySQL server';
$strCantLoad = 'cannot load %s extension,<br />please check PHP Configuration';
$strCantLoadMySQL = 'cannot load MySQL extension,<br />please check PHP Configuration.';
$strCantLoadRecodeIconv = 'Can not load iconv or recode extension needed for charset conversion, configure php to allow using these extensions or disable charset conversion in phpMyAdmin.';
$strCantRenameIdxToPrimary = 'Can\'t rename index to PRIMARY!';
$strCantUseRecodeIconv = 'Can not use iconv nor libiconv nor recode_string function while extension reports to be loaded. Check your php configuration.';
$strCardinality = 'Cardinality';
$strCarriage = 'Carriage return: \\r';
$strChange = 'Change';
$strChangeCopyMode = 'Create a new user with the same privileges and ...';  
$strChangeCopyModeCopy = '... keep the old one.';  
$strChangeCopyModeDeleteAndReload = ' ... delete the old one from the user tables and reload the privileges afterwards.';  
$strChangeCopyModeJustDelete = ' ... delete the old one from the user tables.';  
$strChangeCopyModeRevoke = ' ... revoke all active privileges from the old one and delete it afterwards.';  
$strChangeCopyUser = 'Change Login Information / Copy User';  
$strChangeDisplay = 'Choose Field to display';
$strChangePassword = 'Change password';
$strCharset = 'Charset';
$strCharsetOfFile = 'Character set of the file:';
$strCheckAll = 'Check All';
$strCheckDbPriv = 'Check Database Privileges';
$strCheckPrivs = 'Check Privileges';
$strCheckPrivsLong = 'Check privileges for database &quot;%s&quot;.';
$strCheckTable = 'Check table';
$strChoosePage = 'Please choose a Page to edit';
$strColComFeat = 'Displaying Column Comments';
$strColumn = 'Column';
$strColumnNames = 'Column names';
$strColumnPrivileges = 'Column-specific privileges';
$strCommand = 'Command';
$strComments = 'Comments';
$strCompleteInserts = 'Complete inserts';
$strCompression = 'Compression';
$strConfigFileError = 'phpMyAdmin was unable to read your configuration file!<br />This might happen if php finds a parse error in it or php cannot find the file.<br />Please call the configuration file directly using the link below and read the php error message(s) that you receive. In most cases a quote or a semicolon is missing somewhere.<br />If you receive a blank page, everything is fine.';
$strConfigureTableCoord = 'Please configure the coordinates for table %s';
$strConfirm = 'Do you really want to do it?';
$strConnections = 'Connections';
$strCookiesRequired = 'Cookies must be enabled past this point.';
$strCopyTable = 'Copy table to (database<b>.</b>table):';
$strCopyTableOK = 'Table %s has been copied to %s.';
$strCouldNotKill = 'phpMyAdmin was unable to kill thread %s. It probably has already been closed.';
$strCreate = 'Create';
$strCreateIndex = 'Create an index on&nbsp;%s&nbsp;columns';
$strCreateIndexTopic = 'Create a new index';
$strCreateNewDatabase = 'Create new database';
$strCreateNewTable = 'Create new table on database %s';
$strCreatePage = 'Create a new Page';
$strCreatePdfFeat = 'Creation of PDFs';
$strCriteria = 'Criteria';

$strDBComment = 'Database comment: ';
$strDBGContext = 'Context';
$strDBGContextID = 'Context ID';
$strDBGHits = 'Hits';
$strDBGLine = 'Line';
$strDBGMaxTimeMs = 'Min time, ms';
$strDBGMinTimeMs = 'Max time, ms';
$strDBGModule = 'Module';
$strDBGTimePerHitMs = 'Time/Hit, ms';
$strDBGTotalTimeMs = 'Total time, ms';
$strData = 'Data';
$strDataDict = 'Data Dictionary';
$strDataOnly = 'Data only';
$strDatabase = 'Database ';
$strDatabaseHasBeenDropped = 'Database %s has been dropped.';
$strDatabaseWildcard = 'Database (wildcards allowed):';
$strDatabases = 'Databases';
$strDatabasesDropped = '%s databases have been dropped successfully.';
$strDatabasesStats = 'Databases statistics';
$strDatabasesStatsDisable = 'Disable Statistics';
$strDatabasesStatsEnable = 'Enable Statistics';
$strDatabasesStatsHeavyTraffic = 'Note: Enabling the Database statistics here might cause heavy traffic between the webserver and the MySQL one.';
$strDbPrivileges = 'Database-specific privileges';
$strDbSpecific = 'database-specific';  
$strDefault = 'Default';
$strDefaultValueHelp = 'For default values, please enter just a single value, without backslash escaping or quotes, using this format: a';
$strDelOld = 'The current Page has References to Tables that no longer exist. Would you like to delete those References?';
$strDelete = 'Delete';
$strDeleteAndFlush = 'Delete the users and reload the privileges afterwards.';
$strDeleteAndFlushDescr = 'This is the cleanest way, but reloading the privileges may take a while.';
$strDeleteFailed = 'Deleted Failed!';
$strDeleteUserMessage = 'You have deleted the user %s.';
$strDeleted = 'The row has been deleted';
$strDeletedRows = 'Deleted rows:';
$strDeleting = 'Deleting %s';
$strDescending = 'Descending';
$strDisabled = 'Disabled';
$strDisplay = 'Display';
$strDisplayFeat = 'Display Features';
$strDisplayOrder = 'Display order:';
$strDisplayPDF = 'Display PDF schema';
$strDoAQuery = 'Do a "query by example" (wildcard: "%")';
$strDoYouReally = 'Do you really want to ';
$strDocu = 'Documentation';
$strDrop = 'Drop';
$strDropDB = 'Drop database %s';
$strDropSelectedDatabases = 'Drop Selected Databases';
$strDropTable = 'Drop table';
$strDropUsersDb = 'Drop the databases that have the same names as the users.';
$strDumpComments = 'Include column comments as inline SQL-comments';
$strDumpXRows = 'Dump %s row(s) starting at record # %s.';
$strDumpingData = 'Dumping data for table';
$strDynamic = 'dynamic';

$strEdit = 'Edit';
$strEditPDFPages = 'Edit PDF Pages';
$strEditPrivileges = 'Edit Privileges';
$strEffective = 'Effective';
$strEmpty = 'Empty';
$strEmptyResultSet = 'MySQL returned an empty result set (i.e. zero rows).';
$strEnabled = 'Enabled';
$strEnd = 'End';
$strEndCut = 'END CUT';
$strEndRaw = 'END RAW';
$strEnglishPrivileges = ' Note: MySQL privilege names are expressed in English ';
$strError = 'Error';
$strExplain = 'Explain SQL';
$strExport = 'Export';
$strExportToXML = 'Export to XML format';
$strExtendedInserts = 'Extended inserts';
$strExtra = 'Extra';

$strFailedAttempts = 'Failed attempts';
$strField = 'Field';
$strFieldHasBeenDropped = 'Field %s has been dropped';
$strFields = 'Fields';
$strFieldsEmpty = ' The field count is empty! ';
$strFieldsEnclosedBy = 'Fields enclosed by';
$strFieldsEscapedBy = 'Fields escaped by';
$strFieldsTerminatedBy = 'Fields terminated by';
$strFileCouldNotBeRead = 'File could not be read';
$strFileNameTemplate = 'File name template';
$strFileNameTemplateHelp = 'Use __DB__ for database name, __TABLE__ for table name and %sany strftime%s options for time specification, extension will be automagically added. Any other text will be preserved.';
$strFileNameTemplateRemember = 'remember template';
$strFixed = 'fixed';
$strFlushPrivilegesNote = 'Note: phpMyAdmin gets the users\' privileges directly from MySQL\'s privilege tables. The content of these tables may differ from the privileges the server uses if manual changes have made to it. In this case, you should %sreload the privileges%s before you continue.';
$strFlushTable = 'Flush the table ("FLUSH")';
$strFormEmpty = 'Missing value in the form !';
$strFormat = 'Format';
$strFullText = 'Full Texts';
$strFunction = 'Function';

$strGenBy = 'Generated by';
$strGenTime = 'Generation Time';
$strGeneralRelationFeat = 'General relation features';
$strGlobal = 'global';  
$strGlobalPrivileges = 'Global privileges';
$strGlobalValue = 'Global value';
$strGo = 'Go';
$strGrantOption = 'Grant';
$strGrants = 'Grants';
$strGzip = '"gzipped"';

$strHasBeenAltered = 'has been altered.';
$strHasBeenCreated = 'has been created.';
$strHaveToShow = 'You have to choose at least one Column to display';
$strHome = 'Home';
$strHomepageOfficial = 'Official phpMyAdmin Homepage';
$strHomepageSourceforge = 'Sourceforge phpMyAdmin Download Page';
$strHost = 'Host';
$strHostEmpty = 'The host name is empty!';

$strId = 'ID';
$strIdxFulltext = 'Fulltext';
$strIfYouWish = 'If you wish to load only some of a table\'s columns, specify a comma separated field list.';
$strIgnore = 'Ignore';
$strIgnoringFile = 'Ignoring file %s';
$strImportDocSQL = 'Import docSQL Files';
$strImportFiles = 'Import files';
$strImportFinished = 'Import finished';
$strInUse = 'in use';
$strIndex = 'Index';
$strIndexHasBeenDropped = 'Index %s has been dropped';
$strIndexName = 'Index name&nbsp;:';
$strIndexType = 'Index type&nbsp;:';
$strIndexes = 'Indexes';
$strInnodbStat = 'InnoDB Status';
$strInsecureMySQL = 'Your configuration file contains settings (root with no password) that correspond to the default MySQL privileged account. Your MySQL server is running with this default, is open to intrusion, and you really should fix this security hole.';
$strInsert = 'Insert';
$strInsertAsNewRow = 'Insert as a new row';
$strInsertNewRow = 'Insert new row';
$strInsertTextfiles = 'Insert data from a textfile into table';
$strInsertedRows = 'Inserted rows:';
$strInstructions = 'Instructions';
$strInvalidName = '"%s" is a reserved word, you can\'t use it as a database/table/field name.';

$strJumpToDB = 'Jump to database &quot;%s&quot;.';
$strJustDelete = 'Just delete the users from the privilege tables.';
$strJustDeleteDescr = 'The &quot;deleted&quot; users will still be able to access the server as usual until the privileges are reloaded.';

$strKeepPass = 'Do not change the password';
$strKeyname = 'Keyname';
$strKill = 'Kill';

$strLaTeX = 'LaTeX';
$strLandscape = 'Landscape';
$strLength = 'Length';
$strLengthSet = 'Length/Values*';
$strLimitNumRows = 'Number of rows per page';
$strLineFeed = 'Linefeed: \\n';
$strLines = 'Lines';
$strLinesTerminatedBy = 'Lines terminated by';
$strLinkNotFound = 'Link not found';
$strLinksTo = 'Links to';
$strLocalhost = 'Local';
$strLocationTextfile = 'Location of the textfile';
$strLogPassword = 'Password:';
$strLogUsername = 'Username:';
$strLogin = 'Login';
$strLoginInformation = 'Login Information';
$strLogout = 'Log out';

$strMIME_MIMEtype = 'MIME-type';
$strMIME_available_mime = 'Available MIME-types';
$strMIME_available_transform = 'Available transformations';
$strMIME_description = 'Description';
$strMIME_file = 'Filename';
$strMIME_nodescription = 'No Description is available for this transformation.<br />Please ask the author, what %s does.';
$strMIME_transformation = 'Browser transformation';
$strMIME_transformation_note = 'For a list of available transformation options and their MIME-type transformations, click on %stransformation descriptions%s';
$strMIME_transformation_options = 'Transformation options';
$strMIME_transformation_options_note = 'Please enter the values for transformation options using this format: \'a\',\'b\',\'c\'...<br />If you ever need to put a backslash ("\") or a single quote ("\'") amongst those values, backslashes it (for example \'\\\\xyz\' or \'a\\\'b\').';
$strMIME_without = 'MIME-types printed in italics do not have a seperate transformation function';
$strMissingBracket = 'Missing Bracket';
$strModifications = 'Modifications have been saved';
$strModify = 'Modify';
$strModifyIndexTopic = 'Modify an index';
$strMoreStatusVars = 'More status variables';
$strMoveTable = 'Move table to (database<b>.</b>table):';
$strMoveTableOK = 'Table %s has been moved to %s.';
$strMySQLCharset = 'MySQL charset';
$strMySQLReloaded = 'MySQL reloaded.';
$strMySQLSaid = 'MySQL said: ';
$strMySQLServerProcess = 'MySQL %pma_s1% running on %pma_s2% as %pma_s3%';
$strMySQLShowProcess = 'Show processes';
$strMySQLShowStatus = 'Show MySQL runtime information';
$strMySQLShowVars = 'Show MySQL system variables';

$strName = 'Name';
$strNext = 'Next';
$strNo = 'No';
$strNoDatabases = 'No databases';
$strNoDatabasesSelected = 'No databases selected.';
$strNoDescription = 'no Description';
$strNoDropDatabases = '"DROP DATABASE" statements are disabled.';
$strNoExplain = 'Skip Explain SQL';
$strNoFrames = 'phpMyAdmin is more friendly with a <b>frames-capable</b> browser.';
$strNoIndex = 'No index defined!';
$strNoIndexPartsDefined = 'No index parts defined!';
$strNoModification = 'No change';
$strNoOptions = 'This format has no options';
$strNoPassword = 'No Password';
$strNoPhp = 'Without PHP Code';
$strNoPrivileges = 'No Privileges';
$strNoQuery = 'No SQL query!';
$strNoRights = 'You don\'t have enough rights to be here right now!';
$strNoTablesFound = 'No tables found in database.';
$strNoUsersFound = 'No user(s) found.';
$strNoUsersSelected = 'No users selected.';
$strNoValidateSQL = 'Skip Validate SQL';
$strNone = 'None';
$strNotNumber = 'This is not a number!';
$strNotOK = 'not OK';
$strNotSet = '<b>%s</b> table not found or not set in %s';
$strNotValidNumber = ' is not a valid row number!';
$strNull = 'Null';
$strNumSearchResultsInTable = '%s match(es) inside table <i>%s</i>';
$strNumSearchResultsTotal = '<b>Total:</b> <i>%s</i> match(es)';
$strNumTables = 'Tables';

$strOK = 'OK';
$strOftenQuotation = 'Often quotation marks. OPTIONALLY means that only char and varchar fields are enclosed by the "enclosed by"-character.';
$strOperations = 'Operations';
$strOptimizeTable = 'Optimize table';
$strOptionalControls = 'Optional. Controls how to write or read special characters.';
$strOptionally = 'OPTIONALLY';
$strOptions = 'Options';
$strOr = 'Or';
$strOverhead = 'Overhead';

$strPHP40203 = 'You are using PHP 4.2.3, which has a serious bug with multi-byte strings (mbstring). See PHP bug report 19404. This version of PHP is not recommended for use with phpMyAdmin.';
$strPHPVersion = 'PHP Version';
$strPageNumber = 'Page number:';
$strPartialText = 'Partial Texts';
$strPassword = 'Password';
$strPasswordChanged = 'The Password for %s was changed successfully.';
$strPasswordEmpty = 'The password is empty!';
$strPasswordNotSame = 'The passwords aren\'t the same!';
$strPdfDbSchema = 'Schema of the the "%s" database - Page %s';
$strPdfInvalidPageNum = 'Undefined PDF page number!';
$strPdfInvalidTblName = 'The "%s" table doesn\'t exist!';
$strPdfNoTables = 'No tables';
$strPerHour = 'per hour';
$strPerMinute = 'per minute';
$strPerSecond = 'per second';
$strPhp = 'Create PHP Code';
$strPmaDocumentation = 'phpMyAdmin documentation';
$strPmaUriError = 'The <tt>$cfg[\'PmaAbsoluteUri\']</tt> directive MUST be set in your configuration file!';
$strPortrait = 'Portrait';
$strPos1 = 'Begin';
$strPrevious = 'Previous';
$strPrimary = 'Primary';
$strPrimaryKey = 'Primary key';
$strPrimaryKeyHasBeenDropped = 'The primary key has been dropped';
$strPrimaryKeyName = 'The name of the primary key must be... PRIMARY!';
$strPrimaryKeyWarning = '("PRIMARY" <b>must</b> be the name of and <b>only of</b> a primary key!)';
$strPrint = 'Print';
$strPrintView = 'Print view';
$strPrivDescAllPrivileges = 'Includes all privileges except GRANT.';
$strPrivDescAlter = 'Allows altering the structure of existing tables.';
$strPrivDescCreateDb = 'Allows creating new databases and tables.';
$strPrivDescCreateTbl = 'Allows creating new tables.';
$strPrivDescCreateTmpTable = 'Allows creating temporary tables.';
$strPrivDescDelete = 'Allows deleting data.';
$strPrivDescDropDb = 'Allows dropping databases and tables.';
$strPrivDescDropTbl = 'Allows dropping tables.';
$strPrivDescExecute = 'Allows running stored procedures; Has no effect in this MySQL version.';
$strPrivDescFile = 'Allows importing data from and exporting data into files.';
$strPrivDescGrant = 'Allows adding users and privileges without reloading the privilege tables.';
$strPrivDescIndex = 'Allows creating and dropping indexes.';
$strPrivDescInsert = 'Allows inserting and replacing data.';
$strPrivDescLockTables = 'Allows locking tables for the current thread.';
$strPrivDescMaxConnections = 'Limits the number of new connections the user may open per hour.';
$strPrivDescMaxQuestions = 'Limits the number of queries the user may send to the server per hour.';
$strPrivDescMaxUpdates = 'Limits the number of commands that change any table or database the user may execute per hour.';
$strPrivDescProcess3 = 'Allows killing processes of other users.';
$strPrivDescProcess4 = 'Allows viewing the complete queries in the process list.';
$strPrivDescReferences = 'Has no effect in this MySQL version.';
$strPrivDescReload = 'Allows reloading server settings and flushing the server\'s caches.';
$strPrivDescReplClient = 'Gives the right to the user to ask where the slaves / masters are.';
$strPrivDescReplSlave = 'Needed for the replication slaves.';
$strPrivDescSelect = 'Allows reading data.';
$strPrivDescShowDb = 'Gives access to the complete list of databases.';
$strPrivDescShutdown = 'Allows shutting down the server.';
$strPrivDescSuper = 'Allows connecting, even if maximum number of connections is reached; Required for most administrative operations like setting global variables or killing threads of other users.';
$strPrivDescUpdate = 'Allows changing data.';
$strPrivDescUsage = 'No privileges.';
$strPrivileges = 'Privileges';
$strPrivilegesReloaded = 'The privileges were reloaded successfully.';
$strProcesslist = 'Process list';
$strProperties = 'Properties';
$strPutColNames = 'Put fields names at first row';

$strQBE = 'Query';
$strQBEDel = 'Del';
$strQBEIns = 'Ins';
$strQueryFrame = 'Query window';
$strQueryFrameDebug = 'Debugging information';
$strQueryFrameDebugBox = 'Active variables for the query form:\nDB: %s\nTable: %s\nServer: %s\n\nCurrent variables for the query form:\nDB: %s\nTable: %s\nServer: %s\n\nOpener location: %s\nFrameset location: %s.';
$strQueryOnDb = 'SQL-query on database <b>%s</b>:';
$strQuerySQLHistory = 'SQL-history';
$strQueryStatistics = '<b>Query statistics</b>: Since its startup, %s queries have been sent to the server.';
$strQueryTime = 'Query took %01.4f sec';
$strQueryType = 'Query type';

$strReType = 'Re-type';
$strReceived = 'Received';
$strRecords = 'Records';
$strReferentialIntegrity = 'Check referential integrity:';
$strRelationNotWorking = 'The additional Features for working with linked Tables have been deactivated. To find out why click %shere%s.';
$strRelationView = 'Relation view';
$strRelationalSchema = 'Relational schema';
$strReloadFailed = 'MySQL reload failed.';
$strReloadMySQL = 'Reload MySQL';
$strReloadingThePrivileges = 'Reloading the privileges';
$strRememberReload = 'Remember to reload the server.';
$strRemoveSelectedUsers = 'Remove selected users';
$strRenameTable = 'Rename table to';
$strRenameTableOK = 'Table %s has been renamed to %s';
$strRepairTable = 'Repair table';
$strReplace = 'Replace';
$strReplaceTable = 'Replace table data with file';
$strReset = 'Reset';
$strResourceLimits = 'Resource limits';
$strRevoke = 'Revoke';
$strRevokeAndDelete = 'Revoke all active privileges from the users and delete them afterwards.';
$strRevokeAndDeleteDescr = 'The users will still have the USAGE privilege until the privileges are reloaded.';
$strRevokeGrant = 'Revoke Grant';
$strRevokeGrantMessage = 'You have revoked the Grant privilege for %s';
$strRevokeMessage = 'You have revoked the privileges for %s';
$strRevokePriv = 'Revoke Privileges';
$strRowLength = 'Row length';
$strRowSize = ' Row size ';
$strRows = 'Rows';
$strRowsFrom = 'row(s) starting from record #';
$strRowsModeFlippedHorizontal = 'horizontal (rotated headers)';
$strRowsModeHorizontal = 'horizontal';
$strRowsModeOptions = 'in %s mode and repeat headers after %s cells';
$strRowsModeVertical = 'vertical';
$strRowsStatistic = 'Row Statistic';
$strRunQuery = 'Submit Query';
$strRunSQLQuery = 'Run SQL query/queries on database %s';
$strRunning = 'running on %s';

$strSQL = 'SQL';
$strSQLOptions = 'SQL options';
$strSQLParserBugMessage = 'There is a chance that you may have found a bug in the SQL parser. Please examine your query closely, and check that the quotes are correct and not mis-matched. Other possible failure causes may be that you are uploading a file with binary outside of a quoted text area. You can also try your query on the MySQL command line interface. The MySQL server error output below, if there is any, may also help you in diagnosing the problem. If you still have problems or if the parser fails where the command line interface succeeds, please reduce your SQL query input to the single query that causes problems, and submit a bug report with the data chunk in the CUT section below:';
$strSQLParserUserError = 'There seems to be an error in your SQL query. The MySQL server error output below, if there is any, may also help you in diagnosing the problem';
$strSQLQuery = 'SQL-query';
$strSQLResult = 'SQL result';
$strSQPBugInvalidIdentifer = 'Invalid Identifer';
$strSQPBugUnclosedQuote = 'Unclosed quote';
$strSQPBugUnknownPunctuation = 'Unknown Punctuation String';
$strSave = 'Save';
$strScaleFactorSmall = 'The scale factor is too small to fit the schema on one page';
$strSearch = 'Search';
$strSearchFormTitle = 'Search in database';
$strSearchInTables = 'Inside table(s):';
$strSearchNeedle = 'Word(s) or value(s) to search for (wildcard: "%"):';
$strSearchOption1 = 'at least one of the words';
$strSearchOption2 = 'all words';
$strSearchOption3 = 'the exact phrase';
$strSearchOption4 = 'as regular expression';
$strSearchResultsFor = 'Search results for "<i>%s</i>" %s:';
$strSearchType = 'Find:';
$strSelect = 'Select';
$strSelectADb = 'Please select a database';
$strSelectAll = 'Select All';
$strSelectFields = 'Select fields (at least one):';
$strSelectNumRows = 'in query';
$strSelectTables = 'Select Tables';
$strSend = 'Save as file';
$strSent = 'Sent';
$strServer = 'Server %s';
$strServerChoice = 'Server Choice';
$strServerStatus = 'Runtime Information';
$strServerStatusUptime = 'This MySQL server has been running for %s. It started up on %s.';
$strServerTabProcesslist = 'Processes';
$strServerTabVariables = 'Variables';
$strServerTrafficNotes = '<b>Server traffic</b>: These tables show the network traffic statistics of this MySQL server since its startup.';
$strServerVars = 'Server variables and settings';
$strServerVersion = 'Server version';
$strSessionValue = 'Session value';
$strSetEnumVal = 'If field type is "enum" or "set", please enter the values using this format: \'a\',\'b\',\'c\'...<br />If you ever need to put a backslash ("\") or a single quote ("\'") amongst those values, backslashes it (for example \'\\\\xyz\' or \'a\\\'b\').';
$strShow = 'Show';
$strShowAll = 'Show all';
$strShowColor = 'Show color';
$strShowCols = 'Show columns';
$strShowDatadictAs = 'Data Dictionary Format';
$strShowFullQueries = 'Show Full Queries';
$strShowGrid = 'Show grid';
$strShowPHPInfo = 'Show PHP information';
$strShowTableDimension = 'Show dimension of tables';
$strShowTables = 'Show tables';
$strShowThisQuery = ' Show this query here again ';
$strShowingRecords = 'Showing rows';
$strSingly = '(singly)';
$strSize = 'Size';
$strSort = 'Sort';
$strSpaceUsage = 'Space usage';
$strSplitWordsWithSpace = 'Words are separated by a space character (" ").';
$strStatCheckTime = 'Last check';
$strStatCreateTime = 'Creation';
$strStatUpdateTime = 'Last update';
$strStatement = 'Statements';
$strStatus = 'Status';
$strStrucCSV = 'CSV data';
$strStrucData = 'Structure and data';
$strStrucDrop = 'Add \'drop table\'';
$strStrucExcelCSV = 'CSV for Ms Excel data';
$strStrucOnly = 'Structure only';
$strStructPropose = 'Propose table structure';
$strStructure = 'Structure';
$strSubmit = 'Submit';
$strSuccess = 'Your SQL-query has been executed successfully';
$strSum = 'Sum';
$strSwitchToTable = 'Switch to copied table';

$strTable = 'Table';
$strTableComments = 'Table comments';
$strTableEmpty = 'The table name is empty!';
$strTableHasBeenDropped = 'Table %s has been dropped';
$strTableHasBeenEmptied = 'Table %s has been emptied';
$strTableHasBeenFlushed = 'Table %s has been flushed';
$strTableMaintenance = 'Table maintenance';
$strTableOfContents = 'Table of contents';
$strTableStructure = 'Table structure for table';
$strTableType = 'Table type';
$strTables = '%s table(s)';
$strTblPrivileges = 'Table-specific privileges';
$strTextAreaLength = ' Because of its length,<br /> this field might not be editable ';
$strTheContent = 'The content of your file has been inserted.';
$strTheContents = 'The contents of the file replaces the contents of the selected table for rows with identical primary or unique key.';
$strTheTerminator = 'The terminator of the fields.';
$strThisHost = 'This Host';
$strThisNotDirectory = 'This was not a directory';
$strThreadSuccessfullyKilled = 'Thread %s was successfully killed.';
$strTime = 'Time';
$strTotal = 'total';
$strTotalUC = 'Total';
$strTraffic = 'Traffic';
$strTransformation_image_jpeg__inline = 'Displays a clickable thumbnail; options: width,height in pixels (keeps the original ratio)';
$strTransformation_image_jpeg__link = 'Displays a link to this image (direct blob download, i.e.).';
$strTransformation_image_png__inline = 'See image/jpeg: inline';
$strTransformation_text_plain__dateformat = 'Takes a TIME, TIMESTAMP or DATETIME field and formats it using your local dateformat. First option is the offset (in hours) which will be added to the timestamp (Default: 0). Second option is a different dateformat according to the parameters available for PHPs strftime().';
$strTransformation_text_plain__external = 'LINUX ONLY: Launches an external application and feeds the fielddata via standard input. Returns standard output of the application. Default is Tidy, to pretty print HTML code. For security reasons, you have to manually edit the file libraries/transformations/text_plain__external.inc.php and insert the tools you allow to be run. The first option is then the number of the program you want to use and the second option are the parameters for the program. The third parameter, if set to 1 will convert the output using htmlspecialchars() (Default is 1). A fourth parameter, if set to 1 will put a NOWRAP to the content cell so that the whole output will be shown without reformatting (Default 1)';
$strTransformation_text_plain__formatted = 'Preserves original formatting of the field. No Escaping is done.';
$strTransformation_text_plain__imagelink = 'Displays an image and a link, the field contains the filename; first option is a prefix like "http://domain.com/", second option is the width in pixels, third is the height.';
$strTransformation_text_plain__link = 'Displays a link, the field contains the filename; first option is a prefix like "http://domain.com/", second option is a title for the link.';
$strTransformation_text_plain__substr = 'Only shows part of a string. First option is an offset to define where the output of your text starts (Default 0). Second option is an offset how much text is returned. If empty, returns all the remaining text. The third option defines which chars will be appended to the output when a substring is returned (Default: ...) .';
$strTransformation_text_plain__unformatted = 'Displays HTML code as HTML entities. No HTML formatting is shown.';
$strTruncateQueries = 'Truncate Shown Queries';
$strType = 'Type';

$strUncheckAll = 'Uncheck All';
$strUnique = 'Unique';
$strUnselectAll = 'Unselect All';
$strUpdComTab = 'Please see Documentation on how to update your Column_comments Table';
$strUpdatePrivMessage = 'You have updated the privileges for %s.';
$strUpdateProfile = 'Update profile:';
$strUpdateProfileMessage = 'The profile has been updated.';
$strUpdateQuery = 'Update Query';
$strUsage = 'Usage';
$strUseBackquotes = 'Enclose table and field names with backquotes';
$strUseHostTable = 'Use Host Table';
$strUseTables = 'Use Tables';
$strUseTextField = 'Use text field';
$strUser = 'User';
$strUserAlreadyExists = 'The user %s already exists!';
$strUserEmpty = 'The user name is empty!';
$strUserName = 'User name';
$strUserNotFound = 'The selected user was not found in the privilege table.';
$strUserOverview = 'User overview';
$strUsers = 'Users';
$strUsersDeleted = 'The selected users have been deleted successfully.';
$strUsersHavingAccessToDb = 'Users having access to &quot;%s&quot;';  

$strValidateSQL = 'Validate SQL';
$strValidatorError = 'The SQL validator could not be initialized. Please check if you have installed the necessary php extensions as described in the %sdocumentation%s.';
$strValue = 'Value';
$strVar = 'Variable';
$strViewDump = 'View dump (schema) of table';
$strViewDumpDB = 'View dump (schema) of database';

$strWebServerUploadDirectory = 'web-server upload directory';
$strWebServerUploadDirectoryError = 'The directory you set for upload work cannot be reached';
$strWelcome = 'Welcome to %s';
$strWildcard = 'wildcard';  
$strWithChecked = 'With selected:';
$strWritingCommentNotPossible = 'Writing of comment not possible';
$strWritingRelationNotPossible = 'Writing of relation not possible';
$strWrongUser = 'Wrong username/password. Access denied.';

$strXML = 'XML';

$strYes = 'Yes';

$strZeroRemovesTheLimit = 'Note: Setting these options to 0 (zero) removes the limit.';
$strZip = '"zipped"';

?>
