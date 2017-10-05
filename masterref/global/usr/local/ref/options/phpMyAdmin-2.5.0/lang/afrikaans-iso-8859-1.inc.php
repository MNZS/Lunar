<?php
/* $Id: afrikaans-iso-8859-1.inc.php,v 1.72 2003/04/12 20:04:47 rabus Exp $ */

/*
     translated by Andreas Pauley <pauley@buitegroep.org.za>

Dit lyk nogal snaaks in Afrikaans ;-).
Laat weet my asb. as jy aan beter taalgebruik kan dink.
*/

$charset = 'iso-8859-1';
$text_dir = 'ltr'; // ('ltr' for left to right, 'rtl' for right to left)
$left_font_family = 'verdana, arial, helvetica, geneva, sans-serif';
$right_font_family = 'arial, helvetica, geneva, sans-serif';
$number_thousands_separator = ',';
$number_decimal_separator = '.';
// shortcuts for Byte, Kilo, Mega, Giga, Tera, Peta, Exa
$byteUnits = array('Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB');

$day_of_week = array('So', 'Ma', 'Di', 'Wo', 'Do', 'Fr', 'Sa');
$month = array('Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Des');
// See http://www.php.net/manual/en/function.strftime.php to define the
// variable below
$datefmt = '%B %d, %Y at %I:%M %p';

$strAccessDenied = 'Toegang Geweier';
$strAction = 'Aksie';
$strAddDeleteColumn = 'Voeg By/Verwyder Veld Kolomme';
$strAddDeleteRow = 'Voeg By/Verwyder Kriteria Ry';
$strAddNewField = 'Voeg \'n nuwe veld by';
$strAddPriv = 'Voeg nuwe regte by';
$strAddPrivMessage = 'Jy het nuwe regte bygevoeg';
$strAddSearchConditions = 'Voeg soek kriteria by (laaste deel van die "where" in SQL SELECT):';
$strAddToIndex = 'Voeg by indeks &nbsp;%s&nbsp;kolom(me)';
$strAddUser = 'Voeg \'n nuwe gebruiker by';
$strAddUserMessage = 'Jy het \'n nuwe gebruiker bygevoeg.';
$strAffectedRows = 'Geaffekteerde rye:';
$strAfter = 'Na %s';
$strAfterInsertBack = 'Terug na vorige bladsy';
$strAfterInsertNewInsert = 'Voeg \'n nuwe ry by';
$strAll = 'Alle';
$strAllTableSameWidth = 'vertoon alle tabelle met dieselfde wydte?';
$strAlterOrderBy = 'Verander tabel sorteer volgens';
$strAnalyzeTable = 'Analiseer tabel';
$strAnd = 'En';
$strAnIndex = '\'n Indeks is bygevoeg op %s';
$strAny = 'Enige';
$strAnyColumn = 'Enige Kolom';
$strAnyDatabase = 'Enige databasis';
$strAnyHost = 'Enige gasheer (host)';
$strAnyTable = 'Enige tabel';
$strAnyUser = 'Enige gebruiker';
$strAPrimaryKey = '\'n primere sleutel is bygevoeg op %s';
$strAscending = 'Dalend';
$strAtBeginningOfTable = 'By Begin van Tabel';
$strAtEndOfTable = 'By Einde van Tabel';
$strAttr = 'Kenmerke';

$strBack = 'Terug';
$strBeginCut = 'BEGIN UITKNIPSEL';
$strBeginRaw = 'BEGIN ONVERANDERD (RAW)';
$strBinary = 'Biner';
$strBinaryDoNotEdit = 'Biner - moenie verander nie';
$strBookmarkDeleted = 'Die boekmerk is verwyder.';
$strBookmarkLabel = 'Etiket';
$strBookmarkQuery = 'Geboekmerkde SQL-stelling';
$strBookmarkThis = 'Boekmerk hierdie SQL-stelling';
$strBookmarkView = 'Kyk slegs';
$strBrowse = 'Beloer Data';
$strBzip = '"ge-bzip"';

$strCantLoadMySQL = 'kan ongelukkig nie die MySQL module laai nie, <br />kyk asb. na die PHP opstelling.';
$strCantLoadRecodeIconv = 'Kan nie iconv laai nie, of "recode" ekstensie word benodig vir die karakterstel omskakeling, stel PHP op om hierdie ekstensies toe te laat of verwyder karakterstel omskakeling in phpMyAdmin.';
$strCantRenameIdxToPrimary = 'Kannie die indeks hernoem na PRIMARY!';
$strCantUseRecodeIconv = 'Kan nie iconv, libiconv of recode_string funksie gebruik terwyl die extensie homself as gelaai rapporteer nie. Kyk na jou PHP opstelling.';
$strCardinality = 'Cardinality';
$strCarriage = 'Carriage return: \\r';
$strChange = 'Verander';
$strChangeDisplay = 'Kies \'n Veld om te vertoon';
$strChangePassword = 'Verander wagwoord';
$strCharsetOfFile = 'Karakterstel van die leer:';
$strCheckAll = 'Kies Alles';
$strCheckDbPriv = 'Kontroleer Databasis Regte';
$strCheckTable = 'Kontroleer tabel';
$strChoosePage = 'Kies asb. \'n bladsy om te verander';
$strColComFeat = 'Kolom Kommentaar word vertoon';
$strColumn = 'Kolom';
$strColumnNames = 'Kolom name';
$strComments = 'Kommentaar';
$strCompleteInserts = 'Voltooi invoegings';
$strConfigFileError = 'phpMyAdmin was nie in staat om jou konfigurasie leer te lees nie!<br />Dit kan moontlik gebeur wanneer PHP \'n fout in die leer vind of die leer sommer glad nie vind nie.<br />Volg asb. die skakel hieronder om die leer direk te roep, en lees dan enige foutboodskappe. In die meeste gevalle is daar net \'n quote of \'n kommapunt weg erens.<br />Indien jy \'n bladsy kry wat leeg is, is alles klopdisselboom.';
$strConfigureTableCoord = 'Stel asb. die koordinate op van tabel %s';
$strConfirm = 'Wil jy dit regtig doen?';
$strCookiesRequired = 'HTTP Koekies moet van nou af geaktifeer wees.';
$strCopyTable = 'Kopieer tabel na (databasis<b>.</b>tabel):';
$strCopyTableOK = 'Tabel %s is gekopieer na %s.';
$strCreate = 'Skep';
$strCreateIndex = 'Skep \'n indeks op&nbsp;%s&nbsp;kolomme';
$strCreateIndexTopic = 'Skep \'n nuwe indeks';
$strCreateNewDatabase = 'Skep \'n nuwe databasis';
$strCreateNewTable = 'Skep \'n nuwe tabel op databasis %s';
$strCreatePage = 'Skep \'n nuwe bladsy';
$strCreatePdfFeat = 'Skepping van PDF\'s';
$strCriteria = 'Kriteria';

$strData = 'Data';
$strDatabase = 'Databasis ';
$strDatabaseHasBeenDropped = 'Databasis %s is verwyder.';
$strDatabases = 'databasisse';
$strDatabasesStats = 'Databasis statistieke';
$strDatabaseWildcard = 'Databasis (wildcards toegelaat):';
$strDataOnly = 'Slegs Data';
$strDefault = 'Verstekwaarde (default)';
$strDelete = 'Verwyder';
$strDeleted = 'Die ry is verwyder';
$strDeletedRows = 'Verwyderde rye:';
$strDeleteFailed = 'Verwyder aksie het misluk!';
$strDeleteUserMessage = 'Jy het die gebruiker %s verwyder.';
$strDescending = 'Dalend';
$strDisabled = 'Onbeskikbaar';
$strDisplay = 'Vertoon';
$strDisplayFeat = 'Vertoon Funksies';
$strDisplayOrder = 'Vertoon volgorde:';
$strDisplayPDF = 'Vertoon PDF skema';
$strDoAQuery = 'Doen \'n "Navraag dmv Voorbeeld" (wildcard: "%")';
$strDocu = 'Dokumentasie';
$strDoYouReally = 'Wil jy regtig ';
$strDrop = 'Verwyder';
$strDropDB = 'Verwyder databasis %s';
$strDropTable = 'Verwyder tabel';
$strDumpingData = 'Stort data vir tabel';
$strDumpXRows = 'Stort %s rye beginnende by rekord # %s.';
$strDynamic = 'dinamies';

$strEdit = 'Verander';
$strEditPDFPages = 'Verander PDF Bladsye';
$strEditPrivileges = 'Verander Regte';
$strEffective = 'Effektief';
$strEmpty = 'Maak Leeg';
$strEmptyResultSet = 'MySQL het niks teruggegee nie (dus nul rye).';
$strEnabled = 'Beskikbaar';
$strEnd = 'Einde';
$strEndCut = 'EINDE UITKNIPSEL';
$strEndRaw = 'EINDE ONVERANDERD (RAW)';
$strEnglishPrivileges = ' Nota: MySQL regte name word in Engels vertoon ';
$strError = 'Fout';
$strExplain = 'Verduidelik SQL';
$strExport = 'Export';
$strExportToXML = 'Export na XML formaat';
$strExtendedInserts = 'Uitgebreide toevoegings';
$strExtra = 'Ekstra';

$strField = 'Veld';
$strFieldHasBeenDropped = 'Veld %s is verwyder';
$strFields = 'Velde';
$strFieldsEmpty = ' Die veld telling is leeg! ';
$strFieldsEnclosedBy = 'Velde omring met';
$strFieldsEscapedBy = 'Velde ontsnap (escaped) deur';
$strFieldsTerminatedBy = 'Velde beeindig deur';
$strFixed = 'vaste (fixed)';
$strFlushTable = 'Spoel die tabel ("FLUSH")';
$strFormat = 'Formaat';
$strFormEmpty = 'Daar ontbreek \'n waarde in die vorm !';
$strFullText = 'Volle Tekste';
$strFunction = 'Funksie';

$strGenBy = 'Voortgebring deur';
$strGeneralRelationFeat = 'Algemene verwantskap funksies';
$strGenTime = 'Generasie Tyd';
$strGo = 'Gaan';
$strGrants = 'Vergunnings';
$strGzip = '"ge-gzip"';

$strHasBeenAltered = 'is verander.';
$strHasBeenCreated = 'is geskep.';
$strHaveToShow = 'Jy moet ten minste een Kolom kies om te vertoon';
$strHome = 'Tuis';
$strHomepageOfficial = 'Amptelike phpMyAdmin Tuisblad';
$strHomepageSourceforge = 'Sourceforge phpMyAdmin Aflaai bladsy';
$strHost = 'Gasheer (host)';
$strHostEmpty = 'Die gasheer naam is leeg!';

$strIdxFulltext = 'Volteks';
$strIfYouWish = 'Indien jy slegs sommige van \'n tabel se kolomme wil laai, spesifiseer \'n komma-geskeide veldlys.';
$strIgnore = 'Ignoreer';
$strIndex = 'Indeks';
$strIndexes = 'Indekse';
$strIndexHasBeenDropped = 'Indeks %s is verwyder';
$strIndexName = 'Indeks naam&nbsp;:';
$strIndexType = 'Indeks tipe&nbsp;:';
$strInsert = 'Voeg by';
$strInsertAsNewRow = 'Voeg by as \'n nuwe ry';
$strInsertedRows = 'Toegevoegde rye:';
$strInsertNewRow = 'Voeg nuwe ry by';
$strInsertTextfiles = 'Voeg data vanaf \'n teks leer in die tabel in';
$strInstructions = 'Instruksies';
$strInUse = 'in gebruik';
$strInvalidName = '"%s" is \'n gereserveerde woord, jy kan dit nie as \'n databasis/tabel/veld naam gebruik nie.';

$strKeepPass = 'Moenie die wagwoord verander nie';
$strKeyname = 'Sleutelnaam';
$strKill = 'Vermoor';

$strLength = 'Lengte';
$strLengthSet = 'Lengte/Waardes*';
$strLimitNumRows = 'Hoeveelheid rye per bladsy';
$strLineFeed = 'Linefeed: \\n';
$strLines = 'Lyne';
$strLinesTerminatedBy = 'Lyne beeindig deur';
$strLinkNotFound = 'Skakel nie gevind nie';
$strLinksTo = 'Skakels na';
$strLocationTextfile = 'Soek die teksleer';
$strLogin = 'Teken aan';
$strLogout = 'Teken uit';
$strLogPassword = 'Wagwoord:';
$strLogUsername = 'Gebruiker Naam:';

$strMissingBracket = 'Hakie Ontbreek';
$strModifications = 'Veranderinge is gestoor';
$strModify = 'Verander';
$strModifyIndexTopic = 'Verander \'n indeks';
$strMoveTable = 'Skuif tabel na (databasis<b>.</b>tabel):';
$strMoveTableOK = 'Tabel %s is geskuif na %s.';
$strMySQLCharset = 'MySQL Karakterstel';
$strMySQLReloaded = 'MySQL is herlaai.';
$strMySQLSaid = 'MySQL het gepraat: ';
$strMySQLServerProcess = 'MySQL %pma_s1% hardloop op %pma_s2% as %pma_s3%';
$strMySQLShowProcess = 'Wys prosesse';
$strMySQLShowStatus = 'Wys MySQL in-proses informasie';
$strMySQLShowVars = 'Wys MySQL stelsel veranderlikes';

$strName = 'Naam';
$strNext = 'Volgende';
$strNo = 'Nee';
$strNoDatabases = 'Geen databasisse';
$strNoDescription = 'geen Beskrywing';
$strNoDropDatabases = '"DROP DATABASE" stellings word nie toegelaat nie.';
$strNoExplain = 'Ignoreer SQL Verduideliking';
$strNoFrames = 'phpMyAdmin verkies \'n <b>frames-kapabele</b> blaaier.';
$strNoIndex = 'Geen indeks gedefinieer!';
$strNoIndexPartsDefined = 'Geen indeks dele gedefinieer!';
$strNoModification = 'Geen verandering';
$strNone = 'Geen';
$strNoPassword = 'Geen Wagwoord';
$strNoPhp = 'Sonder PHP Kode';
$strNoPrivileges = 'Geen Regte';
$strNoQuery = 'Geen SQL stelling!';
$strNoRights = 'Jy het nie genoeg regte om nou hier te wees nie!';
$strNoTablesFound = 'Geen tabelle in databasis gevind nie.';
$strNotNumber = 'Hierdie is nie \'n nommer nie';
$strNotOK = 'nie OK';
$strNotSet = '<b>%s</b> tabel nie gevind nie of nie gesetel in %s';
$strNotValidNumber = ' is nie \'n geldige ry-nommer nie!';
$strNoUsersFound = 'Geen gebruiker(s) gevind nie.';
$strNoValidateSQL = 'Ignoreer SQL Validasie';
$strNull = 'Null';
$strNumSearchResultsInTable = '%s resultate binne tabel <i>%s</i>';
$strNumSearchResultsTotal = '<b>Totaal:</b> <i>%s</i> ooreenkomste';

$strOftenQuotation = 'Dikwels kwotasie-karakters. OPSIONEEL beteken dat slegs char en varchar velde ingeslote is binne die "enclosed by"-character.';
$strOK = 'OK';
$strOperations = 'Operasies';
$strOptimizeTable = 'Optimaliseer tabel';
$strOptionalControls = 'Opsioneel. Kontroleer hoe om spesiale karakters te lees en skryf.';
$strOptionally = 'OPSIONEEL';
$strOptions = 'Opsies';
$strOr = 'Of';
$strOverhead = 'Overhead';

$strPageNumber = 'Bladsy nommer:';
$strPartialText = 'Gedeeltelike Tekste';
$strPassword = 'Wagwoord';
$strPasswordEmpty = 'Die wagwoord is leeg!';
$strPasswordNotSame = 'Die wagwoorde is verskillend!';
$strPdfDbSchema = 'Skema van die "%s" databasis - Bladsy %s';
$strPdfInvalidPageNum = 'Ongedefinieerde PDF bladsy nommer!';
$strPdfInvalidTblName = 'Die "%s" databasis bestaan nie!';
$strPdfNoTables = 'Geen tabelle';
$strPhp = 'Skep PHP Kode';
$strPHPVersion = 'PHP Version';
$strPmaDocumentation = 'phpMyAdmin dokumentasie';
$strPmaUriError = 'Die <tt>$cfg[\'PmaAbsoluteUri\']</tt> veranderlike MOET gestel wees in jou konfigurasie leer!';
$strPos1 = 'Begin';
$strPrevious = 'Vorige';
$strPrimary = 'Primere';
$strPrimaryKey = 'Primere sleutel';
$strPrimaryKeyHasBeenDropped = 'Die primere sleutel is verwyder';
$strPrimaryKeyName = 'Die naam van die primere sleutel moet PRIMARY wees!';
$strPrimaryKeyWarning = '("PRIMARY" <b>moet</b> die naam wees van die primere sleutel, en <b>slegs</b> van die primere sleutel!)';
$strPrintView = 'Drukker mooi (print view)';
$strPrivileges = 'Regte';
$strProperties = 'Eienskappe';

$strQBE = 'Navraag dmv Voorbeeld';
$strQBEDel = 'Del';
$strQBEIns = 'Ins';
$strQueryOnDb = 'SQL-navraag op databasis <b>%s</b>:';

$strRecords = 'Rekords';
$strReferentialIntegrity = 'Toets referential integrity:';
$strRelationNotWorking = 'Die addisionele funksies om met geskakelde tabelle te werk is ge deaktiveer. Om uit te vind hoekom kliek %shier%s.';
$strRelationView = 'Relasie uitsig';
$strReloadFailed = 'MySQL herlaai het misluk.';
$strReloadMySQL = 'Herlaai MySQL';
$strRememberReload = 'Onthou om die bediener (server) te herlaai.';
$strRenameTable = 'Hernoem tabel na';
$strRenameTableOK = 'Tabel %s is vernoem na %s';
$strRepairTable = 'Herstel tabel';
$strReplace = 'Vervang';
$strReplaceTable = 'Vervang tabel data met leer (file)';
$strReset = 'Herstel';
$strReType = 'Tik weer';
$strRevoke = 'Herroep';
$strRevokeGrant = 'Herroep Vergunning';
$strRevokeGrantMessage = 'Jy het die Vergunnings-reg herroep vir %s';
$strRevokeMessage = 'Jy het die regte herroep vir %s';
$strRevokePriv = 'Herroep Regte';
$strRowLength = 'Ry lengte';
$strRows = 'Rye';
$strRowsFrom = 'ry(e) beginnende vanaf rekord #';
$strRowSize = ' Ry grootte ';
$strRowsModeHorizontal = 'horisontale';
$strRowsModeOptions = 'in %s formaat en herhaal opskrifte na %s selle';
$strRowsModeVertical = 'vertikale';
$strRowsStatistic = 'Ry Statistiek';
$strRunning = 'op bediener %s';
$strRunQuery = 'Doen Navraag';
$strRunSQLQuery = 'Hardloop SQL stellings op databasis %s';

$strSave = 'Stoor';
$strScaleFactorSmall = 'Die skaal faktor is te klein om die skema op een bladsy te pas';
$strSearch = 'Soek';
$strSearchFormTitle = 'Soek in databasis';
$strSearchInTables = 'Binne tabel(le):';
$strSearchNeedle = 'Woord(e) of waarde(s) om voor te soek (wildcard: "%"):';
$strSearchOption1 = 'ten minste een van die woorde';
$strSearchOption2 = 'alle woorde';
$strSearchOption3 = 'die presiese frase';
$strSearchOption4 = 'as \'n regular expression';
$strSearchResultsFor = 'Soek resultate vir "<i>%s</i>" %s:';
$strSearchType = 'Vind:';
$strSelect = 'Kies';
$strSelectADb = 'Kies asb. \'n databasis';
$strSelectAll = 'Kies Alles';
$strSelectFields = 'Kies Velde (ten minste een):';
$strSelectNumRows = 'in navraag';
$strSelectTables = 'Kies Tabelle';
$strSend = 'Stoor as leer (file)';
$strServerChoice = 'Bediener Keuse';
$strServerVersion = 'Bediener weergawe';
$strSetEnumVal = 'If field type is "enum" or "set", please enter the values using this format: \'a\',\'b\',\'c\'...<br />If you ever need to put a backslash ("\") or a single quote ("\'") amongst those values, backslashes it (for example \'\\\\xyz\' or \'a\\\'b\').';
$strShow = 'Wys';
$strShowAll = 'Wys alles';
$strShowColor = 'Wys kleur';
$strShowCols = 'Wys kolomme';
$strShowGrid = 'Wys ruitgebied';
$strShowingRecords = 'Vertoon rye';
$strShowPHPInfo = 'Wys PHP informasie';
$strShowTableDimension = 'Wys dimensie van tabelle';
$strShowTables = 'Wys tabelle';
$strShowThisQuery = ' Wys hierdie navraag weer hier ';
$strSingly = '(afsonderlik)';
$strSize = 'Grootte';
$strSort = 'Sorteer';
$strSpaceUsage = 'Spasie verbruik';
$strSplitWordsWithSpace = 'Woorde is geskei dmv \'n spasie karakter (" ").';
$strSQL = 'SQL';
$strSQLParserBugMessage = 'Jy het moontlik \'n fout in die SQL interpreteerder ontdek. Ondersoek asb. jou stelling deeglik, en maak seker dat jou kwotasies korrek en gebalanseerd is. Ander moontlike oorsake vir die fout mag wees dat jy probeer om \'n leer in te laai met binere data buite \'n gekwoteerde teks area. Jy kan jou SQL stelling ook probeer direk in die MySQL opdrag-raakvlak (command line interface). Die MySQL bediener se foutboodskap hieronder (indien enige) kan jou ook help om die probleem te diagnoseer. As jy dan nog steeds probleme het, of as die interpreteerder fouteer waar die opdrag-raakvlak slaag, verminder asb. jou SQL stelling toevoer na die enkele stelling wat die probleem veroorsaak, en rapporteer \'n fout met die data stuk in die UITKNIPSEL seksie hieronder:';
$strSQLParserUserError = 'Dit lyk of daar \'n fout is in jou SQL stelling. Die MySQL bediener se foutboodskap hieronder (indien enige) kan jou ook help om die probleem te diagnoseer';
$strSQLQuery = 'SQL-stelling';
$strSQLResult = 'SQL resultaat';
$strSQPBugInvalidIdentifer = 'Ongeldige Identifiseerder';
$strSQPBugUnclosedQuote = 'Ongebalanseerde kwotasie-teken';
$strSQPBugUnknownPunctuation = 'Onbekende Punktuasie String';
$strStatement = 'Stellings';
$strStrucCSV = 'CSV data';
$strStrucData = 'Struktuur en data';
$strStrucDrop = 'Voeg \'drop table\' by';
$strStrucExcelCSV = 'CSV vir M$ Excel data';
$strStrucOnly = 'Slegs struktuur';
$strStructPropose = 'Stel tabel struktuur voor';
$strStructure = 'Struktuur';
$strSubmit = 'Stuur';
$strSuccess = 'Jou SQL-navraag is suksesvol uitgevoer';
$strSum = 'Som';

$strTable = 'Tabel';
$strTableComments = 'Tabel kommentaar';
$strTableEmpty = 'Die tabel naam is leeg!';
$strTableHasBeenDropped = 'Tabel %s is verwyder';
$strTableHasBeenEmptied = 'Tabel %s is leeg gemaak';
$strTableHasBeenFlushed = 'Tabel %s is geflush';
$strTableMaintenance = 'Tabel instandhouding';
$strTables = '%s tabel(le)';
$strTableStructure = 'Tabel struktuur vir tabel';
$strTableType = 'Tabel tipe';
$strTextAreaLength = ' Omrede sy lengte,<br /> is hierdie veld moontlik nie veranderbaar nie ';
$strTheContent = 'Die inhoud van jou leer is ingevoeg.';
$strTheContents = 'Die inhoud van die leer vervang die inhoud van die geselekteerde tabel vir rye met \'n identiese primere of unieke sleutel.';
$strTheTerminator = 'Die beeindiger (terminator) van die velde.';
$strTotal = 'totaal';
$strType = 'Tipe';

$strUncheckAll = 'Kies Niks';
$strUnique = 'Uniek';
$strUnselectAll = 'Selekteer Niks';
$strUpdatePrivMessage = 'Jy het die regte opgedateer vir %s.';
$strUpdateProfile = 'Verander profiel:';
$strUpdateProfileMessage = 'Die profiel is opgedateer.';
$strUpdateQuery = 'Verander Navraag';
$strUsage = 'Gebruik';
$strUseBackquotes = 'Omring tabel en veldname met backquotes';
$strUser = 'Gebruiker';
$strUserEmpty = 'Die gebruiker naam ontbreek!';
$strUserName = 'Gebruiker naam';
$strUsers = 'Gebruikers';
$strUseTables = 'Gebruik Tabelle';

$strValidateSQL = 'Valideer SQL';
$strValue = 'Waarde';
$strViewDump = 'Sien die storting (skema) van die tabel';
$strViewDumpDB = 'Sien die storting (skema) van die databasis';

$strWelcome = 'Welkom by %s';
$strWithChecked = 'Met gekose:';
$strWrongUser = 'Verkeerde gebruikernaam/wagwoord. Toegang geweier.';

$strYes = 'Ja';

$strZip = '"ge-zip"';

$strInsecureMySQL = 'Your configuration file contains settings (root with no password) that correspond to the default MySQL privileged account. Your MySQL server is running with this default, is open to intrusion, and you really should fix this security hole.';  //to translate
$strWebServerUploadDirectory = 'web-server upload directory';  //to translate
$strWebServerUploadDirectoryError = 'The directory you set for upload work cannot be reached';  //to translate
$strValidatorError = 'The SQL validator could not be initialized. Please check if you have installed the necessary php extensions as described in the %sdocumentation%s.'; //to translate
$strServer = 'Server %s';  //to translate
$strPutColNames = 'Put fields names at first row';  //to translate
$strImportDocSQL = 'Import docSQL Files';  //to translate
$strDataDict = 'Data Dictionary';  //to translate
$strPrint = 'Print';  //to translate
$strPHP40203 = 'You are using PHP 4.2.3, which has a serious bug with multi-byte strings (mbstring). See PHP bug report 19404. This version of PHP is not recommended for use with phpMyAdmin.';  //to translate
$strCompression = 'Compression'; //to translate
$strNumTables = 'Tables'; //to translate
$strTotalUC = 'Total'; //to translate
$strRelationalSchema = 'Relational schema';  //to translate
$strTableOfContents = 'Table of contents';  //to translate
$strCannotLogin = 'Cannot login to MySQL server';  //to translate
$strShowDatadictAs = 'Data Dictionary Format';  //to translate
$strLandscape = 'Landscape';  //to translate
$strPortrait = 'Portrait';  //to translate

$timespanfmt = '%s days, %s hours, %s minutes and %s seconds'; //to translate

$strAbortedClients = 'Aborted'; //to translate
$strConnections = 'Connections'; //to translate
$strFailedAttempts = 'Failed attempts'; //to translate
$strGlobalValue = 'Global value'; //to translate
$strMoreStatusVars = 'More status variables'; //to translate
$strPerHour = 'per hour'; //to translate
$strQueryStatistics = '<b>Query statistics</b>: Since its startup, %s queries have been sent to the server.';
$strQueryType = 'Query type'; //to translate
$strReceived = 'Received'; //to translate
$strSent = 'Sent'; //to translate
$strServerStatus = 'Runtime Information'; //to translate
$strServerStatusUptime = 'This MySQL server has been running for %s. It started up on %s.'; //to translate
$strServerTabVariables = 'Variables'; //to translate
$strServerTabProcesslist = 'Processes'; //to translate
$strServerTrafficNotes = '<b>Server traffic</b>: These tables show the network traffic statistics of this MySQL server since its startup.';
$strServerVars = 'Server variables and settings'; //to translate
$strSessionValue = 'Session value'; //to translate
$strTraffic = 'Traffic'; //to translate
$strVar = 'Variable'; //to translate

$strCommand = 'Command'; //to translate
$strCouldNotKill = 'phpMyAdmin was unable to kill thread %s. It probably has already been closed.'; //to translate
$strId = 'ID'; //to translate
$strProcesslist = 'Process list'; //to translate
$strStatus = 'Status'; //to translate
$strTime = 'Time'; //to translate
$strThreadSuccessfullyKilled = 'Thread %s was successfully killed.'; //to translate

$strBzError = 'phpMyAdmin was unable to compress the dump because of a broken Bz2 extension in this php version. It is strongly recommended to set the <code>$cfg[\'BZipDump\']</code> directive in your phpMyAdmin configuration file to <code>FALSE</code>. If you want to use the Bz2 compression features, you should upgrade to a later php version. See php bug report %s for details.'; //to translate
$strLaTeX = 'LaTeX';  //to translate

$strAdministration = 'Administration'; //to translate
$strFlushPrivilegesNote = 'Note: phpMyAdmin gets the users\' privileges directly from MySQL\'s privilege tables. The content of this tables may differ from the privileges the server uses if manual changes have made to it. In this case, you should %sreload the privileges%s before you continue.'; //to translate
$strGlobalPrivileges = 'Global privileges'; //to translate
$strGrantOption = 'Grant'; //to translate
$strPrivDescAllPrivileges = 'Includes all privileges except GRANT.'; //to translate
$strPrivDescAlter = 'Allows altering the structure of existing tables.'; //to translate
$strPrivDescCreateDb = 'Allows creating new databases and tables.'; //to translate
$strPrivDescCreateTbl = 'Allows creating new tables.'; //to translate
$strPrivDescCreateTmpTable = 'Allows creating temporary tables.'; //to translate
$strPrivDescDelete = 'Allows deleting data.'; //to translate
$strPrivDescDropDb = 'Allows dropping databases and tables.'; //to translate
$strPrivDescDropTbl = 'Allows dropping tables.'; //to translate
$strPrivDescExecute = 'Allows running stored procedures; Has no effect in this MySQL version.'; //to translate
$strPrivDescFile = 'Allows importing data from and exporting data into files.'; //to translate
$strPrivDescGrant = 'Allows adding users and privileges without reloading the privilege tables.'; //to translate
$strPrivDescIndex = 'Allows creating and dropping indexes.'; //to translate
$strPrivDescInsert = 'Allows inserting and replacing data.'; //to translate
$strPrivDescLockTables = 'Allows locking tables for the current thread.'; //to translate
$strPrivDescMaxConnections = 'Limits the number of new connections the user may open per hour.';
$strPrivDescMaxQuestions = 'Limits the number of queries the user may send to the server per hour.';
$strPrivDescMaxUpdates = 'Limits the number of commands that change any table or database the user may execute per hour.';
$strPrivDescProcess3 = 'Allows killing processes of other users.'; //to translate
$strPrivDescProcess4 = 'Allows viewing the complete queries in the process list.'; //to translate
$strPrivDescReferences = 'Has no effect in this MySQL version.'; //to translate
$strPrivDescReplClient = 'Gives the right to the user to ask where the slaves / masters are.'; //to translate
$strPrivDescReplSlave = 'Needed for the replication slaves.'; //to translate
$strPrivDescReload = 'Allows reloading server settings and flushing the server\'s caches.'; //to translate
$strPrivDescSelect = 'Allows reading data.'; //to translate
$strPrivDescShowDb = 'Gives access to the complete list of databases.'; //to translate
$strPrivDescShutdown = 'Allows shutting down the server.'; //to translate
$strPrivDescSuper = 'Allows connectiong, even if maximum number of connections is reached; Required for most administrative operations like setting global variables or killing threads of other users.'; //to translate
$strPrivDescUpdate = 'Allows changing data.'; //to translate
$strPrivDescUsage = 'No privileges.'; //to translate
$strPrivilegesReloaded = 'The privileges were reloaded successfully.'; //to translate
$strResourceLimits = 'Resource limits'; //to translate
$strUserOverview = 'User overview'; //to translate
$strZeroRemovesTheLimit = 'Note: Setting these options to 0 (zero) removes the limit.'; //to translate

$strPasswordChanged = 'The Password for %s was changed successfully.'; // to translate

$strDeleteAndFlush = 'Delete the users and reload the privileges afterwards.'; //to translate
$strDeleteAndFlushDescr = 'This is the cleanest way, but reloading the privileges may take a while.'; //to translate
$strDeleting = 'Deleting %s'; //to translate
$strJustDelete = 'Just delete the users from the privilege tables.'; //to translate
$strJustDeleteDescr = 'The &quot;deleted&quot; users will still be able to access the server as usual until the privileges are reloaded.'; //to translate
$strReloadingThePrivileges = 'Reloading the privileges'; //to translate
$strRemoveSelectedUsers = 'Remove selected users'; //to translate
$strRevokeAndDelete = 'Revoke all active privileges from the users and delete them afterwards.'; //to translate
$strRevokeAndDeleteDescr = 'The users will still have the USAGE privilege until the privileges are reloaded.'; //to translate
$strUsersDeleted = 'The selected users have been deleted successfully.'; //to translate

$strAddPrivilegesOnDb = 'Add privileges on the following database'; //to translate
$strAddPrivilegesOnTbl = 'Add privileges on the following table'; //to translate
$strColumnPrivileges = 'Column-specific privileges'; //to translate
$strDbPrivileges = 'Database-specific privileges'; //to translate
$strLocalhost = 'Local';
$strLoginInformation = 'Login Information'; //to translate
$strTblPrivileges = 'Table-specific privileges'; //to translate
$strThisHost = 'This Host'; //to translate
$strUserNotFound = 'The selected user was not found in the privilege table.'; //to translate
$strUserAlreadyExists = 'The user %s already exists!'; //to translate
$strUseTextField = 'Use text field'; //to translate

$strNoUsersSelected = 'No users selected.'; //to translate
$strDropUsersDb = 'Drop the databases that have the same names as the users.'; //to translate
$strAddedColumnComment = 'Added comment for column';  //to translate
$strWritingCommentNotPossible = 'Writing of comment not possible';  //to translate
$strAddedColumnRelation = 'Added relation for column';  //to translate
$strWritingRelationNotPossible = 'Writing of relation not possible';  //to translate
$strImportFinished = 'Import finished';  //to translate
$strFileCouldNotBeRead = 'File could not be read';  //to translate
$strIgnoringFile = 'Ignoring file %s';  //to translate
$strThisNotDirectory = 'This was not a directory';  //to translate
$strAbsolutePathToDocSqlDir = 'Please enter the absolute path on webserver to docSQL directory';  //to translate
$strImportFiles = 'Import files';  //to translate
$strDBGModule = 'Module';  //to translate
$strDBGLine = 'Line';  //to translate
$strDBGHits = 'Hits';  //to translate
$strDBGTimePerHitMs = 'Time/Hit, ms';  //to translate
$strDBGTotalTimeMs = 'Total time, ms';  //to translate
$strDBGMinTimeMs = 'Min time, ms';  //to translate
$strDBGMaxTimeMs = 'Max time, ms';  //to translate
$strDBGContextID = 'Context ID';  //to translate
$strDBGContext = 'Context';  //to translate
$strCantLoad = 'cannot load %s extension,<br />please check PHP Configuration';  //to translate
$strDefaultValueHelp = 'For default values, please enter just a single value, without backslash escaping or quotes, using this format: a';  //to translate
$strCheckPrivs = 'Check Privileges';  //to translate
$strCheckPrivsLong = 'Check privileges for database &quot;%s&quot;.';  //to translate
$strDatabasesStatsHeavyTraffic = 'Note: Enabling the Database statistics here might cause heavy traffic between the webserver and the MySQL one.';  //to translate
$strDatabasesStatsDisable = 'Disable Statistics';  //to translate
$strDatabasesStatsEnable = 'Enable Statistics';  //to translate
$strJumpToDB = 'Jump to database &quot;%s&quot;.';  //to translate
$strDropSelectedDatabases = 'Drop Selected Databases';  //to translate
$strNoDatabasesSelected = 'No databases selected.';  //to translate
$strDatabasesDropped = '%s databases have been dropped successfully.';  //to translate
$strGlobal = 'global';  //to translate
$strDbSpecific = 'database-specific';  //to translate
$strUsersHavingAccessToDb = 'Users having access to &quot;%s&quot;';  //to translate
$strChangeCopyUser = 'Change Login Information / Copy User';  //to translate
$strChangeCopyMode = 'Create a new user with the same privileges and ...';  //to translate
$strChangeCopyModeCopy = '... keep the old one.';  //to translate
$strChangeCopyModeJustDelete = ' ... delete the old one from the user tables.';  //to translate
$strChangeCopyModeRevoke = ' ... revoke all active privileges from the old one and delete it afterwards.';  //to translate
$strChangeCopyModeDeleteAndReload = ' ... delete the old one from the user tables and reload the privileges afterwards.';  //to translate
$strWildcard = 'wildcard';  //to translate
$strRowsModeFlippedHorizontal = 'horizontal (rotated headers)';//to translate
$strQueryTime = 'Query took %01.4f sec';//to translate
$strDumpComments = 'Include column comments as inline SQL-comments';//to translate
$strDBComment = 'Database comment: ';//to translate
$strQueryFrame = 'Query window';//to translate
$strQueryFrameDebug = 'Debugging information';//to translate
$strQueryFrameDebugBox = 'Active variables for the query form:\nDB: %s\nTable: %s\nServer: %s\n\nCurrent variables for the query form:\nDB: %s\nTable: %s\nServer: %s\n\nOpener location: %s\nFrameset location: %s.';//to translate
$strQuerySQLHistory = 'SQL-history';//to translate
$strMIME_MIMEtype = 'MIME-type';//to translate
$strMIME_transformation = 'Browser transformation';//to translate
$strMIME_transformation_options = 'Transformation options';//to translate
$strMIME_transformation_options_note = 'Please enter the values for transformation options using this format: \'a\',\'b\',\'c\'...<br />If you ever need to put a backslash ("\") or a single quote ("\'") amongst those values, backslashes it (for example \'\\\\xyz\' or \'a\\\'b\').';//to translate
$strMIME_transformation_note = 'For a list of available transformation options and their MIME-type transformations, click on %stransformation descriptions%s';//to translate
$strMIME_available_mime = 'Available MIME-types';//to translate
$strMIME_available_transform = 'Available transformations';//to translate
$strMIME_without = 'MIME-types printed in italics do not have a seperate transformation function';//to translate
$strMIME_description = 'Description';//to translate
$strMIME_nodescription = 'No Description is available for this transformation.<br />Please ask the author, what %s does.';//to translate
$strMIME_file = 'Filename';//to translate
$strTransformation_text_plain__formatted = 'Preserves original formatting of the field. No Escaping is done.';//to translate
$strTransformation_text_plain__unformatted = 'Displays HTML code as HTML entities. No HTML formatting is shown.';//to translate
$strTransformation_image_jpeg__link = 'Displays a link to this image (direct blob download, i.e.).';//to translate
$strInnodbStat = 'InnoDB Status';  //to translate
$strUpdComTab = 'Please see Documentation on how to update your Column_comments Table';  //to translate
$strTransformation_image_jpeg__inline = 'Displays a clickable thumbnail; options: width,height in pixels (keeps the original ratio)';  //to translate
$strTransformation_image_png__inline = 'See image/jpeg: inline';  //to translate
$strSQLOptions = 'SQL options';//to translate
$strXML = 'XML';//to translate
$strCSVOptions = 'CSV options';//to translate
$strNoOptions = 'This format has no options';//to translate
$strStatCreateTime = 'Creation';//to translate
$strStatUpdateTime = 'Last update';//to translate
$strStatCheckTime = 'Last check';//to translate
$strPerMinute = 'per minute';//to translate
$strPerSecond = 'per second';//to translate
$strAutomaticLayout = 'Automatic layout';  //to translate
$strDelOld = 'The current Page has References to Tables that no longer exist. Would you like to delete those References?';  //to translate
$strFileNameTemplate = 'File name template';//to translate 
$strFileNameTemplateRemember = 'remember template';//to translate 
$strFileNameTemplateHelp = 'Use __DB__ for database name, __TABLE__ for table name and %sany strftime%s options for time specification, extension will be automagically added. Any other text will be preserved.';//to translate
$strTransformation_text_plain__dateformat = 'Takes a TIME, TIMESTAMP or DATETIME field and formats it using your local dateformat. First option is the offset (in hours) which will be added to the timestamp (Default: 0). Second option is a different dateformat according to the parameters available for PHPs strftime().';//to translate
$strTransformation_text_plain__substr = 'Only shows part of a string. First option is an offset to define where the output of your text starts (Default 0). Second option is an offset how much text is returned. If empty, returns all the remaining text. The third option defines which chars will be appended to the output when a substring is returned (Default: ...) .';//to translate
$strTransformation_text_plain__external = 'LINUX ONLY: Launches an external application and feeds the fielddata via standard input. Returns standard output of the application. Default is Tidy, to pretty print HTML code. For security reasons, you have to manually edit the file libraries/transformations/text_plain__external.inc.php and insert the tools you allow to be run. The first option is then the number of the program you want to use and the second option are the parameters for the program. The third parameter, if set to 1 will convert the output using htmlspecialchars() (Default is 1). A fourth parameter, if set to 1 will put a NOWRAP to the content cell so that the whole output will be shown without reformatting (Default 1)';//to translate
$strAutodetect = 'Autodetect';  //to translate
$strTransformation_text_plain__imagelink = 'Displays an image and a link, the field contains the filename; first option is a prefix like "http://domain.com/", second option is the width in pixels, third is the height.';  //to translate
$strTransformation_text_plain__link = 'Displays a link, the field contains the filename; first option is a prefix like "http://domain.com/", second option is a title for the link.';  //to translate
$strUseHostTable = 'Use Host Table';  //to translate
$strShowFullQueries = 'Show Full Queries';  //to translate
$strTruncateQueries = 'Truncate Shown Queries';  //to translate
$strSwitchToTable = 'Switch to copied table';  //to translate
$strCharset = 'Charset';  //to translate
?>