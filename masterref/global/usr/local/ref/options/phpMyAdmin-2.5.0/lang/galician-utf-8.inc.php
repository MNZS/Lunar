<?php
/* $Id: galician-utf-8.inc.php,v 1.100 2003/04/12 20:04:58 rabus Exp $ */

/**
 * Translated by Xosé Calvo <xosecalvo at terra.es>
 */

$charset = 'utf-8';
$allow_recoding = TRUE;
$text_dir = 'ltr';
$left_font_family = 'verdana, arial, helvetica, geneva, sans-serif';
$right_font_family = 'arial, helvetica, geneva, sans-serif';
$number_thousands_separator = '.';
$number_decimal_separator = ',';
// shortcuts for Byte, Kilo, Mega, Giga, Tera, Peta, Exa
$byteUnits = array('Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB');

$day_of_week = array('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat');
$month = array('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
// See http://www.php.net/manual/en/function.strftime.php to define the
// variable below
$datefmt = '%B %d, %Y at %I:%M %p';

$timespanfmt = '%s días, %s horas, %s minutos e %s segundos';

$strUpdComTab = 'Consulte a Documentación para saber como actualizar a tabela Column_comments';  

$strAPrimaryKey = 'Adicionouse unha chave primaria a %s';
$strAbortedClients = 'Cancelado';
$strAbsolutePathToDocSqlDir = 'Introduza a rota absoluta completa ao directorio docSQL no servidor';
$strAccessDenied = 'Acceso Negado';
$strAction = 'Acción';
$strAddDeleteColumn = 'Adicionar/Eliminar columnas de campo';
$strAddDeleteRow = 'Adicionar/Eliminar filas de criterios';
$strAddNewField = 'Adicionar un novo campo';
$strAddPriv = 'Adicionar un novo privilexio';
$strAddPrivMessage = 'Privilexio adicionado.';
$strAddPrivilegesOnDb = 'Adicionar privilexios para a esta base de datos';
$strAddPrivilegesOnTbl = 'Adicionar privilexios para a esta tabela';
$strAddSearchConditions = 'Condición da pesquisa (ou sexa, o complemento da cláusula "WHERE"):';
$strAddToIndex = 'Adicionar ao índice &nbsp;%s&nbsp;coluna(s)';
$strAddUser = 'Adicionar un novo usuario';
$strAddUserMessage = 'Usuario adicionado.';
$strAddedColumnComment = 'Púxoselle un comentario á columna';
$strAddedColumnRelation = 'Adicionóuselle unha relación á columna';
$strAdministration = 'Administración';
$strAffectedRows = 'Filas que van ser afectadas:';
$strAfter = 'Despois de %s';
$strAfterInsertBack = 'Voltar';
$strAfterInsertNewInsert = 'Inserir un novo rexistro';
$strAll = 'Todos';
$strAllTableSameWidth = 'mostrar todas as tabelas co mesmo ancho?';
$strAlterOrderBy = 'Ordenar a tabela por';
$strAnIndex = 'Adicionouse un índice a %s';
$strAnalyzeTable = 'Analizar a tabela';
$strAnd = 'E';
$strAny = 'Calquer';
$strAnyColumn = 'Calquer columna';
$strAnyDatabase = 'Calquer banco de datos';
$strAnyHost = 'Calquer servidor';
$strAnyTable = 'Calquer tabela';
$strAnyUser = 'Calquer usuario';
$strAscending = 'Ascendente';
$strAtBeginningOfTable = 'No comezo da tabela';
$strAtEndOfTable = 'Ao final da tabela';
$strAttr = 'Atributos';
$strAutodetect = 'Autodetectar';  
$strAutomaticLayout = 'Distribución automática';  

$strBack = 'Voltar';
$strBeginCut = 'COMEZA O RECORTE';
$strBeginRaw = 'COMEZA O TEXTO SIMPLE ("RAW")';
$strBinary = ' Binario ';
$strBinaryDoNotEdit = ' Binario - non editar ';
$strBookmarkDeleted = 'Eliminouse o marcador.';
$strBookmarkLabel = 'Nome';
$strBookmarkQuery = 'A procura de SQL foi gardada';
$strBookmarkThis = 'Gardar esta procura de SQL';
$strBookmarkView = 'Só visualizar';
$strBrowse = 'Visualizar';
$strBzError = 'phpMyAdmin foi incapaz de comprimir os resultados debido a que esta versión do php ten unha extensión de Bz2 con erros.  Recoméndase que configure a directiva <code>$cfg[\'BZipDump\']</code> do seu ficheiro de configuración do phpMyAdmin para que sexa <code>FALSE</code>. Se quer usar a funcionalidade de compresión Bz2, actualice a unha versión posterior do php. Consulte o informe de erros %s para máis detalles.';
$strBzip = 'comprimido no formato "bzipped"';

$strCSVOptions = 'Opcións CSV';
$strCannotLogin = 'Non podo conectar co servidor de MySQL';
$strCantLoad = 'Non se pode carregar a extensión %s.<br />Comprobe a configuración do PHP.';
$strCantLoadMySQL = 'Non foi posible carregar a extensión do MySQL;<br>comprobe, por favor, a configuración do PHP.';
$strCantLoadRecodeIconv = 'Non se puido carregar iconv ou precísase da extensión recode para a conversión do charset. Configure o php para que se poidan usar estas extensións ou indique que non se use a conversión de charset en phpMyAdmin.';
$strCantRenameIdxToPrimary = 'Non se pode facer que este índice sexa PRIMARIO!';
$strCantUseRecodeIconv = 'Non se puido usar nen iconv nen libiconv nen a función recode_stringf mentres haxa extensións por carregar. Comprobe a súa configuración do php.';
$strCardinality = 'Cardinalidade';
$strCarriage = 'Carácter de retorno: \\r';
$strChange = 'Mudar';
$strChangeCopyMode = 'Crear un utilizador novo cos mesmos privilexios e...';
$strChangeCopyModeCopy = '... manter o anterior.';
$strChangeCopyModeDeleteAndReload = ' ... eliminar o anterior das tabelas de utilizadores e recarregar os privilexios despóis.';
$strChangeCopyModeJustDelete = ' ... eliminar o anterior das tabelas de utilizadores.';
$strChangeCopyModeRevoke = ' ... retirar-lle todos os privilexios activos ao anterior e eliminalo despóis.';
$strChangeCopyUser = 'Modificar a información de acceso (login) / Copiar utilizador';
$strChangeDisplay = 'Escolla o campo que se há de mostrar';
$strChangePassword = 'Trocar o contrasinal';
$strCharsetOfFile = 'Conxunto de caracteres do ficheiro:';
$strCheckAll = 'Marcá-los todos';
$strCheckDbPriv = 'Verificar os privilexios do banco de datos';
$strCheckPrivs = 'Comprobar os privilexios';
$strCheckPrivsLong = 'Comprobar os privilexios da base de datos &quot;%s&quot;.';
$strCheckTable = 'Verificar a tabela';
$strChoosePage = 'Escolla unha páxina para modificar';
$strColComFeat = 'Mostrando os comentarios das columnas';
$strColumn = 'Columna';
$strColumnNames = 'Nomes das Columnas';
$strColumnPrivileges = 'Privilexios proprios de columna';
$strCommand = 'Comando';
$strComments = 'Comentarios';
$strCompleteInserts = 'Insercións completas';
$strCompression = 'Compresión';
$strConfigFileError = 'phpMyAdmin non puido ler o seu ficheiro de configuración<br/>Isto podería deberse a que php atopou un erro nel ou a que php non puido atopar o ficheiro.<br/>Invoque o ficheiro de configuración directamente mediante o vínculo que hai máis abaixo e lea a mensaxe de erro de php que receba. Na maioría dos casos simplesmente faltan unha aspa ou un ponto e vírcula <br/>Se recebe unha páxina en branco é que todo está ben.';
$strConfigureTableCoord = 'Configure as coordenadas da tabela %s';
$strConfirm = 'Está seguro/a?';
$strConnections = 'Conexións';
$strCookiesRequired = 'A partir de aqui debe permitir cookies.';
$strCopyTable = 'Copiar a tabela a (base_de_datos<b>.</b>tabela):';
$strCopyTableOK = 'Tabela \$table copiada para \$new_name.';
$strCouldNotKill = 'phpMyAdmin foi incapaz de finalizar o fío %s.  Probablemente xa está fechado.';
$strCreate = 'Crear';
$strCreateIndex = 'Crear un índice en&nbsp;%s&nbsp;colunas';
$strCreateIndexTopic = 'Crear un novo índice';
$strCreateNewDatabase = 'Crear un novo banco de datos';
$strCreateNewTable = 'Crear unha tabela nova na base de datos %s';
$strCreatePage = 'Crear unha páxina nova';
$strCreatePdfFeat = 'Creación de PDFs';
$strCriteria = 'Criterio';

$strDBComment = 'Comentario da base de datos: ';
$strDBGContext = 'Contexto';
$strDBGContextID = 'ID do contexto';
$strDBGHits = 'Hits';
$strDBGLine = 'Liña';
$strDBGMaxTimeMs = 'Tempo máximo, ms';
$strDBGMinTimeMs = 'Tempo mínimo, ms';
$strDBGModule = 'Módulo';
$strDBGTimePerHitMs = 'Tempo/Hit, ms';
$strDBGTotalTimeMs = 'Tempo total, ms';
$strData = 'Datos';
$strDataDict = 'Diccionario de datos';
$strDataOnly = 'Só os datos';
$strDatabase = 'Banco de Datos ';
$strDatabaseHasBeenDropped = 'A base de datos %s foi eliminada.';
$strDatabaseWildcard = 'Base de datos (permítese usar os comodíns):';
$strDatabases = 'Bancos de Datos';
$strDatabasesDropped = 'Elimináronse %s bases de datos sen problemas.';
$strDatabasesStats = 'Estatísticas dos bancos de datos';
$strDatabasesStatsDisable = 'Deshabilitar as estatísticas';
$strDatabasesStatsEnable = 'Habilitar as estatísticas';
$strDatabasesStatsHeavyTraffic = 'Nota: De habilitar as estatísticas da base de datos, ocasionará que se produza un tráfico denso entre o servidor web e o de MySQL.';
$strDbPrivileges = 'Privilexios proprios de base de datos';
$strDbSpecific = 'específico da base de datos';
$strDefault = 'Padrón';
$strDefaultValueHelp = 'Para os valores por omisión, introduza un único valor, sen escapalo con barras ou aspas e usando este formato: a';
$strDelOld = 'Esta páxina ten referencias a tabelas que xa non existen. Quere eliminar esas referencias?'; 
$strDelete = 'Eliminar';
$strDeleteAndFlush = 'Eliminar os usuarios e recarregar os privilexios a continuación.';
$strDeleteAndFlushDescr = 'Este é o modo máis limpo, mais pode que recarregar os privilexios leve un pouco de tempo.';
$strDeleteFailed = 'Non foi posible eliminar!';
$strDeleteUserMessage = 'Acaba de eliminar o usuario %s.';
$strDeleted = 'Rexistro eliminado';
$strDeletedRows = 'Filas borradas:';
$strDeleting = 'A eliminar %s';
$strDescending = 'Descendente';
$strDisabled = 'Desactivado';
$strDisplay = 'Mostrar';
$strDisplayFeat = 'Mostrar as características';
$strDisplayOrder = 'Mostrar en orde:';
$strDisplayPDF = 'Mostrar o esquema PDF';
$strDoAQuery = 'Faga unha "procura por exemplo" (o comodín é "%")';
$strDoYouReally = 'Seguro? ';
$strDocu = 'Documentación';
$strDrop = 'Eliminar';
$strDropDB = 'Elimina o banco de datos %s';
$strDropSelectedDatabases = 'Eliminar as bases de datos seleccionadas';
$strDropTable = 'Eliminar a tabela';
$strDropUsersDb = 'Eliminar as bases de datos que teñan os mesmos nomes que os usuarios.';
$strDumpComments = 'Incluir os comentarios das columnas como comentarios de SQL na liña';
$strDumpXRows = 'Pór %s filas a partir da fila %s.';
$strDumpingData = 'Extraindo datos da tabela';
$strDynamic = 'dinámico';

$strEdit = 'Modificar';
$strEditPDFPages = 'Editar as páxinas PDF';
$strEditPrivileges = 'Modificar privilexios';
$strEffective = 'Efectivo';
$strEmpty = 'Borrar';
$strEmptyResultSet = 'MySQL retornou um conxunto vacío (ex. cero rexistros).';
$strEnabled = 'Activado';
$strEnd = 'Fin';
$strEndCut = 'FIN DO RECORTE';
$strEndRaw = 'FIN DO TEXTO SIMPLE ("RAW")';
$strEnglishPrivileges = ' Nota: os nomes de privilexios do MySQL están en inglés';
$strError = 'Erro';
$strExplain = 'Explicar SQL';
$strExport = 'Exportar';
$strExportToXML = 'Exportar no formato XML';
$strExtendedInserts = 'Insercións extendidas';
$strExtra = 'Extra';

$strFailedAttempts = 'Tentativas falidas';
$strField = 'Campo';
$strFieldHasBeenDropped = 'Eliminouse o campo %s';
$strFields = 'Campos';
$strFieldsEmpty = ' O reconto de campos di que non hai nengún! ';
$strFieldsEnclosedBy = 'Os campos delimítanse con';
$strFieldsEscapedBy = 'Os campos escápanse con';
$strFieldsTerminatedBy = 'Os campos rematan por';
$strFileCouldNotBeRead = 'Non se puido ler o ficheiro';
$strFileNameTemplate = 'Modelo para o nome de ficheiro'; 
$strFileNameTemplateHelp = 'Usar __DB__ para o nome da base de datos, __TABLE__ para o nome de tabela e opcións %sany strftime%s  para a especificación da hora; a extensión engadirá-se automaxicamenteO rexto do texto manterá-se.';
$strFileNameTemplateRemember = 'lembrar o modelo'; 
$strFixed = 'fixo';
$strFlushPrivilegesNote = 'Nota: phpMyAdmin recolle os privilexios dos usuarios directamente das tabelas de privilexios do MySQL. O contido destas tabelas pode diferir dos privilexios que usa o servidor se se levaron a cabo alteracións manuais.  Neste caso, debería %svolver a carregar os privilexios%s antes de continuar.';
$strFlushTable = 'Fechar a tabela ("FLUSH")';
$strFormEmpty = 'Falta un valor no formulario!';
$strFormat = 'Formato';
$strFullText = 'Textos completos';
$strFunction = 'Funcións';

$strGenBy = 'Xerado por';
$strGenTime = 'Xerado en';
$strGeneralRelationFeat = 'Características xerais das relacións';
$strGlobal = 'global';
$strGlobalPrivileges = 'Privilexios globais';
$strGlobalValue = 'Valor global';
$strGo = 'Executar';
$strGrantOption = 'Conceder';
$strGrants = 'Conceder';
$strGzip = 'comprimido no formato "gzipped"';

$strHasBeenAltered = 'foi alterado.';
$strHasBeenCreated = 'foi creado.';
$strHaveToShow = 'Ten que escoller polo menos unha columna para mostrar';
$strHome = 'Comezo ("Home")';
$strHomepageOfficial = 'Páxina Oficial do phpMyAdmin';
$strHomepageSourceforge = 'Páxina do phpMyAdmin en Sourceforge';
$strHost = 'Servidor';
$strHostEmpty = 'O nome do servidor está vacío!';

$strId = 'ID';
$strIdxFulltext = 'Texto completo';
$strIfYouWish = 'Para carregar só algunhas columnas da tabela, faga unha lista separada por vírgulas.';
$strIgnore = 'Ignorar';
$strIgnoringFile = 'A ignorar o ficheiro %s';
$strImportDocSQL = 'Importar ficheiros de docSQL';
$strImportFiles = 'Importar ficheiros';
$strImportFinished = 'Finalizou a importación';
$strInUse = 'en uso';
$strIndex = 'Índice';
$strIndexHasBeenDropped = 'Eliminouse o índice %s';
$strIndexName = 'Nome do índice&nbsp;:';
$strIndexType = 'Tipo de índice&nbsp;:';
$strIndexes = 'Índices';
$strInnodbStat = 'Estado de InnoDB';  
$strInsecureMySQL = 'O seu ficheiro de configuración contén axustes (en concreto, o usuário root non ten contrasinal) que corresponden coa conta con todos os privilexios que MySQL fai por omisión. O seu servidor de MySQL está a rodar con esta configuración, está aberto a intrusións e habería que mirar de solucionar este problema de seguranza.';
$strInsert = 'Inserir';
$strInsertAsNewRow = 'Inserir unha nova columna';
$strInsertNewRow = 'Inserir un novo rexistro';
$strInsertTextfiles = 'Inserir un arquivo de texto na tabela';
$strInsertedRows = 'Filas inseridas:';
$strInstructions = 'Instruccións';
$strInvalidName = '"%s" i unha palabra reservada. Non se pode utilizar como nome dun banco de datos, dunha tabela ou dun campo.';

$strJumpToDB = 'Saltar à base de datos &quot;%s&quot;.';
$strJustDelete = 'Elimine só os usuarios das tabelas de privilexios.';
$strJustDeleteDescr = 'Os usuarios &quot;eliminados&quot; poderán ainda acceder ao servidor como sempre atá que se recarreguen os privilexios.';

$strKeepPass = 'Non mude o contrasinal';
$strKeyname = 'Nome chave';
$strKill = 'Matar (kill)';

$strLaTeX = 'LaTeX';
$strLandscape = 'Horizontal';
$strLength = 'Tamaño';
$strLengthSet = 'Tamaño/Definir*';
$strLimitNumRows = 'Número de rexistros por páxina';
$strLineFeed = 'Carácter de alimentación de liña: \\n';
$strLines = 'Liñas';
$strLinesTerminatedBy = 'As liñas rematan por';
$strLinkNotFound = 'Non se atopou o vínculo';
$strLinksTo = 'Vincúlase con';
$strLocalhost = 'Local';
$strLocationTextfile = 'Localización do arquivo de texto';
$strLogPassword = 'Contrasinal:';
$strLogUsername = 'Nome de usuario:';
$strLogin = 'Entrada (login)';
$strLoginInformation = 'Información sobre o acceso (login)';
$strLogout = 'Sair';

$strMIME_MIMEtype = 'Tipo MIME';
$strMIME_available_mime = 'Tipos MIME disponibles';
$strMIME_available_transform = 'Transformacións disponibles';
$strMIME_description = 'Descrición';
$strMIME_file = 'Nome de ficheiro';
$strMIME_nodescription = 'Non existe descrición desta transformación.<br />Pergunte-lle ao autor que é o que fai %s.';
$strMIME_transformation = 'Transformación do navegador';
$strMIME_transformation_note = 'Para unha lista das opcións de transformación disponibles e as súas transformacións de tipos MIME, faga clic sobre  %sdescricións de transformacións%s';
$strMIME_transformation_options = 'Opcións de transformación';
$strMIME_transformation_options_note = 'Introduza os valores das opcións de transformación usando este formato:\'a\',\'b\',\'c\'...<br />Se necesita introducir unha barra para trás ("\") ou aspas simples ("\'") entre estes valores, preceda-os de barra para trás (por exemplo \'\\\\xyz\' ou \'a\\\'b\').';
$strMIME_without = 'Os tipos MIME en cursiva non contan cunha función de transformación separada';
$strMissingBracket = 'Falta un paréntese';
$strModifications = 'As modificacións foron gardadas';
$strModify = 'Modificar';
$strModifyIndexTopic = 'Modificar un índice';
$strMoreStatusVars = 'Máis variables de estado';
$strMoveTable = 'Mover a tabela a (base_de_datos<b>.</b>tabela):';
$strMoveTableOK = 'Moveuse a tabela %s para %s.';
$strMySQLCharset = 'Código de caracteres (Charset) MySQL';
$strMySQLReloaded = 'MySQL reiniciado.';
$strMySQLSaid = 'Mensaxes do MySQL: ';
$strMySQLServerProcess = 'MySQL %pma_s1% a rodar no servidor %pma_s2% como %pma_s3%';
$strMySQLShowProcess = 'Mostrar os procesos';
$strMySQLShowStatus = 'Mostrar información de tempo de execución do MySQL';
$strMySQLShowVars = 'Mostrar as variables de sistema do MySQL';

$strName = 'Nome';
$strNext = 'Seguinte';
$strNo = 'Non';
$strNoDatabases = 'Non hai nengún banco de datos';
$strNoDatabasesSelected = 'Non hai nengunha base de datos seleccionada.';
$strNoDescription = 'sen descrición';
$strNoDropDatabases = 'Os comandos "Eliminar banco de datos" non están permitidos.';
$strNoExplain = 'Saltar a explicacion de SQL';
$strNoFrames = 'phpMyAdmin usa-se mellor cun navegador que <b>acepte molduras</b>.';
$strNoIndex = 'Non se definiu un índice';
$strNoIndexPartsDefined = 'Non se definiron partes do índice';
$strNoModification = 'Sen cambios';
$strNoOptions = 'Este formato non ten opcións';
$strNoPassword = 'Sen Contrasinal';
$strNoPhp = 'sen código PHP';
$strNoPrivileges = 'Sen Privilexios';
$strNoQuery = 'Non hai procura SQL!';
$strNoRights = 'Non ten direitos suficientes para estar aquí agora!';
$strNoTablesFound = 'Non se achou nengunha tabela no banco de datos';
$strNoUsersFound = 'Non se achou nengun(s) usuario(s).';
$strNoUsersSelected = 'Non se seleccionou nengun usuario.';
$strNoValidateSQL = 'Saltarse a validacion de';
$strNone = 'Nengun';
$strNotNumber = 'Non é un número!';
$strNotOK = 'non conforme';
$strNotSet = 'Non se atopou a tabela <b>%s</b>ou non se indicou en %s';
$strNotValidNumber = ' non é un número válido para unha fila!';
$strNull = 'Nulo';
$strNumSearchResultsInTable = '%s ocorrencias(s) dentro da tabela <i>%s</i>';
$strNumSearchResultsTotal = '<b>Total:</b> <i>%s</i> ocorrencia(s)';
$strNumTables = 'Tables';

$strOK = 'Conforme';
$strOftenQuotation = 'Xeralmente son aspas. OPCIONAL significa que só os campos de caracteres son delimitados por caracteres "delimitadores"';
$strOperations = 'Operacións';
$strOptimizeTable = 'Optimizar a tabela';
$strOptionalControls = 'Opcional. Controla como se han de ler e escreber os caracteres especiais.';
$strOptionally = 'OPCIONAL';
$strOptions = 'Opcións';
$strOr = 'ou';
$strOverhead = 'De máis (Overhead)';

$strPHP40203 = 'Está a usar PHP 4.2.3, que contén un erro importante relacionado coas cadeas multi-byte (mbstring). Consulte o informe de erros número 19404. Non se recomenda usar esta versión do PHP co phpMyAdmin.';
$strPHPVersion = 'Versión do PHP';
$strPageNumber = 'Número de páxina:';
$strPartialText = 'Textos parciais';
$strPassword = 'Contrasinal';
$strPasswordChanged = 'Modificou-se sen problemas o contrasinal de %s.';
$strPasswordEmpty = 'O contrasinal está vacío!';
$strPasswordNotSame = 'Os contrasinais non son os mesmos!';
$strPdfDbSchema = 'Esquema da base de datos "%s" - Páxina %s';
$strPdfInvalidPageNum = 'O número de páxina PDF non está definido';
$strPdfInvalidTblName = 'Non existe a tabela "%s".';
$strPdfNoTables = 'Sen tabelas';
$strPerHour = 'por hora';
$strPerMinute = 'por minuto';
$strPerSecond = 'por segundo';
$strPhp = 'Crear código PHP';
$strPmaDocumentation = 'Documentación do phpMyAdmin';
$strPmaUriError = 'A directiva <tt>$cfg[\'PmaAbsoluteUri\']</tt> DEBE estar asignada no seu ficheiro de configuración.';
$strPortrait = 'Vertical';
$strPos1 = 'Inicio';
$strPrevious = 'Anterior';
$strPrimary = 'Primaria';
$strPrimaryKey = 'Chave primaria';
$strPrimaryKeyHasBeenDropped = 'Eliminouse a chave primaria';
$strPrimaryKeyName = 'O nome da chave primaria debe ser... PRIMARIA';
$strPrimaryKeyWarning = '("PRIMARIA" <b>debe</b> ser o nome de e <b>só de</b> unha chave primaria)';
$strPrint = 'Imprimir';
$strPrintView = 'Visualización previa da impresión';
$strPrivDescAllPrivileges = 'Inclue todos os privilexios a excepción de GRANT (Conceder).';
$strPrivDescAlter = 'Permite alterar a estrutura das tabelas xa existentes.';
$strPrivDescCreateDb = 'Permite crear novas bases de datos e tabelas.';
$strPrivDescCreateTbl = 'Permite crear tabelas novas.';
$strPrivDescCreateTmpTable = 'Permite crear tabelas temporais.';
$strPrivDescDelete = 'Permite eliminar datos.';
$strPrivDescDropDb = 'Permite eliminar bases de datos e tabelas.';
$strPrivDescDropTbl = 'Permite eliminar tabelas.';
$strPrivDescExecute = 'Permite facer correr procedimentos armacenados. Non funciona nesta versión do MySQL.';
$strPrivDescFile = 'Permite importar e exportar datos desde e para ficheiros.';
$strPrivDescGrant = 'Permite acrescentar usuarios e privilexios sen recarregar as tabelas de privilexios.';
$strPrivDescIndex = 'Permite crear e eliminar índices.';
$strPrivDescInsert = 'Permite inserir e substituir datos.';
$strPrivDescLockTables = 'Permite bloquear tabelas do fío en uso';
$strPrivDescMaxConnections = 'Limita o número de conexións novas por hora que pode abrir un usuario.';
$strPrivDescMaxQuestions = 'Limita o número de procuras por hora que pode enviar un usuario.';
$strPrivDescMaxUpdates = 'Limita o número de comandos que modifiquen unha tabela ou database por hora que pode executar un usuario.';
$strPrivDescProcess3 = 'Permite matar procesos pertencentes a outros usuarios.';
$strPrivDescProcess4 = 'Permite ver as procuras completas na listaxe de procesos.';
$strPrivDescReferences = 'Non funciona nesta versión do MySQL.';
$strPrivDescReload = 'Permite recarregar a configuración do servidor e limpar a súa caché.';
$strPrivDescReplClient = 'Permite-lle ao usuario perguntar onde están os escravos e os masters.';
$strPrivDescReplSlave = 'Necesario para os escravos de replicación.';
$strPrivDescSelect = 'Permite gravar datos.';
$strPrivDescShowDb = 'Permite acceder á listaxe de bases de datos completa';
$strPrivDescShutdown = 'Permite apagar o servidor.';
$strPrivDescSuper = 'Permite conexións, mesmo chegado ao número máximo de conexións. Ven requerido para a maioría das operación administracións, como configurar as variábeis globais ou matar os fíos doutros usuarios.';
$strPrivDescUpdate = 'Permite modificar datos.';
$strPrivDescUsage = 'Sen privilexios.';
$strPrivileges = 'Privilexios';
$strPrivilegesReloaded = 'Non houbo problemas ao recarregar os privilexios.';
$strProcesslist = 'Listaxe dos procesos';
$strProperties = 'Propiedades';
$strPutColNames = 'Pór os nomes dos campos na primeira fileira';

$strQBE = 'Procurar pondo un exemplo ("QBE")';
$strQBEDel = 'Eliminar';
$strQBEIns = 'Inserir';
$strQueryFrame = 'Xanela de procuras';
$strQueryFrameDebug = 'Información sobre o erro';
$strQueryFrameDebugBox = 'Variables activas para o formulario de procura:\nBase de datos: %s\nTabela: %s\nServidor: %s\n\nVariables actuais do formulario de procura: \nBase de datos: %s\nTabela: %s\nServidor: %s\n\nLocalización do abridor: %s\nLocalización do frameset: %s.';
$strQueryOnDb = 'Procura tipo SQL no banco de datos <b>%s</b>:';
$strQuerySQLHistory = 'Historial de SQL';
$strQueryStatistics = '<b>Estatística das procuras</b>: Desde que se iniciou, enviáronselle ao servidor %s procuras.';
$strQueryTime = 'A pesquisa levou %01.4f segundos';
$strQueryType = 'Tipo de procura';

$strReType = 'Reescreber';
$strReceived = 'Recibido';
$strRecords = 'Rexistros';
$strReferentialIntegrity = 'Comprobar a integridade das referencias:';
$strRelationNotWorking = 'Desactivouse a funcionalidade adicional para o traballo con tabelas vinculadas. Para saber o por que, faga click%saqu&iacute;%s.';
$strRelationView = 'Vista das relacións';
$strRelationalSchema = 'Relational schema';
$strReloadFailed = 'A reinicialización do MySQL fallou.';
$strReloadMySQL = 'Reinicializar o MySQL';
$strReloadingThePrivileges = 'A recarregar os privilexios';
$strRememberReload = 'Lembre-se recarregar o servidor.';
$strRemoveSelectedUsers = 'Eliminar os usuarios seleccionados';
$strRenameTable = 'Renomear a tabela para';
$strRenameTableOK = 'Tabela \$table renomeada para \$new_name';
$strRepairTable = 'Reparar a tabela';
$strReplace = 'Substituir';
$strReplaceTable = 'Substituir os datos da tabela polos do ficheiro';
$strReset = 'Reiniciar';
$strResourceLimits = 'Limites de recursos';
$strRevoke = 'Revogar';
$strRevokeAndDelete = 'Retirar-lles todos os privilexios activos aos usuarios e eliminá-los a continuación.';
$strRevokeAndDeleteDescr = 'Os usuarios terán ainda o privilexio USAGE até que se recarreguen os privilexios.';
$strRevokeGrant = 'Revogar privilexio de conceder';
$strRevokeGrantMessage = 'Retirou-lle o privilexio de Permitir a %s';
$strRevokeMessage = 'Retirou-lle os privilexios a %s';
$strRevokePriv = 'Revogar privilexios';
$strRowLength = 'Lonxitude da fila';
$strRowSize = ' Tamaño da fila ';
$strRows = 'Filas';
$strRowsFrom = 'filas, a comezar da';
$strRowsModeFlippedHorizontal = 'horizontal (cabezallos rotados)';
$strRowsModeHorizontal = 'horizontal';
$strRowsModeOptions = 'en modo %s e repetir os cabezallos de cada %s celas';
$strRowsModeVertical = 'vertical';
$strRowsStatistic = 'Estatistícas da Fila';
$strRunQuery = 'Enviar esta procura';
$strRunSQLQuery = 'Efectuar unha procura SQL na base de datos %s';
$strRunning = 'a rodar no servidor %s';

$strSQL = 'SQL';
$strSQLOptions = 'Opcións SQL';
$strSQLParserBugMessage = 'Cabe a posibilidade de que atopase un erro no procesador de SQL. Examine a súa pesquisa con atención e comprobe que as aspas son correctas e que teñen o seu par. Outras causas posibles póden-se deber a que tentase enviar un ficheiro con binario fora dunha área de texto entre aspas. Tamén pode tentar facer a súa pesquisa na liña de comandos de MySQL. A mensaxe de erro que lle envía o servidor de MySQL e que aparece máis abaixo (de habela) tamén o pode axudar a diagnosticar o problema. Se persisten os erros ou se o procesador falla cando mesmo a liña de comandos vai ben,reduza o texto da pesquisa à parte concreta que produce o erro e envíe unha mensaxe de erro co texto da sección RECORTE que aparece a continuación:';
$strSQLParserUserError = 'Parece que houbo un problema na súa pesquisa en SQL. Se máis abaixo aparece unha mensaxe de erro do servidor de MySQL, isto pode axudar a diagnosticar o problema';
$strSQLQuery = 'comando SQL';
$strSQLResult = 'Resultado SQL';
$strSQPBugInvalidIdentifer = 'O identificador non é válido';
$strSQPBugUnclosedQuote = 'Falta pór a aspa final';
$strSQPBugUnknownPunctuation = 'Hai unha secuencia de puntuación que resulta descoñecida';
$strSave = 'Gardar';
$strScaleFactorSmall = 'O factor de reducción é demasiado pequeno para que o esquema caiba nunha única páxina';
$strSearch = 'Procurar';
$strSearchFormTitle = 'Procurar na base de datos';
$strSearchInTables = 'Dentro da(s) tabela(s):';
$strSearchNeedle = 'Palabras(s) ou valore(s) a procurar (o comodín é: "%"):';
$strSearchOption1 = 'polo menos unha das palabras';
$strSearchOption2 = 'todas as palabras';
$strSearchOption3 = 'a frase exacta';
$strSearchOption4 = 'como expresión regular';
$strSearchResultsFor = 'Procurar os resultados para "<i>%s</i>" %s:';
$strSearchType = 'Atopar:';
$strSelect = 'Procurar';
$strSelectADb = 'Seleccione unha base de dados';
$strSelectAll = 'Seleccionar todo';
$strSelectFields = 'Seleccione os campos (mínimo 1)';
$strSelectNumRows = 'a procurar';
$strSelectTables = 'Seleccionar tabelas';
$strSend = 'Enviar <I>(gravar nun ficheiro)</I><br>';
$strSent = 'Enviado';
$strServer = 'Servidor %s';
$strServerChoice = 'Escolla de Servidor';
$strServerStatus = 'Información sobre o runtime';
$strServerStatusUptime = 'Este servidor de MySQL leva funcionando %s. Iniciouse às %s.';
$strServerTabProcesslist = 'Procesos';
$strServerTabVariables = 'Variábeis';
$strServerTrafficNotes = '<b>Tráfico do servidor</b>: Estas tabelas mostran as estatísticas do tráfico da rede neste servidor de MySQL desde que se iniciou.';
$strServerVars = 'Variables e configuración do servidor';
$strServerVersion = 'Versión do servidor';
$strSessionValue = 'Valor da sesión';
$strSetEnumVal = 'Se o tipo de campo é "enum" ou "set", introduza os valores usando este formato: \'a\',\'b\',\'c\'...<br />Se precisar pór unha barra invertida (" \ ") ou aspas simples (" \' ") entre estes valores, preceda a barra e as aspas de barras invertidas (por exemplo \'\\\\xyz\' ou \'a\\\'b\').';
$strShow = 'Mostrar';
$strShowAll = 'Ver todos os rexistros';
$strShowColor = 'Mostrar a cor';
$strShowCols = 'Mostrar as columnas';
$strShowDatadictAs = 'Formato do diccionario de datos';
$strShowFullQueries = 'Mostrar as procuras completas';  
$strShowGrid = 'Mostrar a grella';
$strShowPHPInfo = 'Mostrar información sobre o PHP';
$strShowTableDimension = 'Mostrar a dimensión das tabelas';
$strShowTables = 'Mostrar as tabelas';
$strShowThisQuery = ' Mostrar esta procura aquí outra vez ';
$strShowingRecords = 'Mostrando rexistros ';
$strSingly = 'a refacer logo de insercións e destrucións (shingly)';
$strSize = 'Tamaño';
$strSort = 'Ordenar';
$strSpaceUsage = 'Uso do espazo';
$strSplitWordsWithSpace = 'As palabras divídense cun carácter de espazo (" ").';
$strStatCheckTime = 'Comprobación máis recente';
$strStatCreateTime = 'Creación';
$strStatUpdateTime = 'Actualización máis recente';
$strStatement = 'Informacións';
$strStatus = 'Estado';
$strStrucCSV = 'Datos CSV';
$strStrucData = 'Estructura e datos';
$strStrucDrop = 'Adicionar \'Eliminar tabela anterior se existe\'';
$strStrucExcelCSV = 'CSV (para datos de Ms Excel)';
$strStrucOnly = 'Só a estructura';
$strStructPropose = 'Propor unha estructura para a tabela';
$strStructure = 'Estructura';
$strSubmit = 'Submeter';
$strSuccess = 'O seu comando de SQL executou-se com éxito';
$strSum = 'Suma';

$strTable = 'Tabela';
$strTableComments = 'Comentarios da tabela';
$strTableEmpty = 'O nome da tabela está vacío!';
$strTableHasBeenDropped = 'Eliminouse a tabela %s';
$strTableHasBeenEmptied = 'Vaciouse a tabela %s';
$strTableHasBeenFlushed = 'Fechouse a tabela %s';
$strTableMaintenance = 'Tabela de manutención';
$strTableOfContents = 'Table of contents';
$strTableStructure = 'Estructura da tabela';
$strTableType = 'Tipo da tabela';
$strTables = '%s tabela(s)';
$strTblPrivileges = 'Privilexios proprios de tabela';
$strTextAreaLength = ' Por causa da sua lonxitude,<br> este campo pode non ser editable ';
$strTheContent = 'O conteúdo do seu arquivo foi inserido';
$strTheContents = 'O conteúdo do arquivo substituíu o conteúdo da tabela que tiña a mesma chave primaria ou única';
$strTheTerminator = 'O carácter que separa os campos.';
$strThisHost = 'Este servidor';
$strThisNotDirectory = 'Isto non era un directorio';
$strThreadSuccessfullyKilled = 'Finalizouse o fío %s.';
$strTime = 'Tempo';
$strTotal = 'total';
$strTotalUC = 'Total';
$strTraffic = 'Tráfico';
$strTransformation_image_jpeg__inline = 'Mostra unha imaxe reducida vinculable. Opcións: ancho,alto en píxeles (mantén a proporción orixinal)';
$strTransformation_image_jpeg__link = 'Mostra un vínculo a esta imaxe (ou sexa, baixada directa de blob).';
$strTransformation_image_png__inline = 'Ver image/jpeg: na liña';  
$strTransformation_text_plain__dateformat = 'Colle un campo TIME, TIMESTAMP ou DATETIME field e formata-o usando o seu formato de data local.  A primeira opción é offset (en horas), que se engadirá á marca horaria (timestamp, por omisión, 0). A segunda opción é un formato de data diferente dependendo dos parámetros disponibles para a función strftime() do PHP.';
$strTransformation_text_plain__formatted = 'Mantén o formato orixinal do campo. Non hai Escape.';
$strTransformation_text_plain__imagelink = 'Mostra unha imaxe e un vínculo; o campo conte o nome do ficheiro. A primeira opción é un prefixo do tipo "http://domain.com/"; a segunda opción é o ancho en píxeles; a terceira é a altura.'; 
$strTransformation_text_plain__link = 'Mostra un vínculo; o campo contén o nome do ficheiro. A primeira opción é un prefixo do tipo "http://domain.com/"; a segunda opción é un título para o vínculo.'; 
$strTransformation_text_plain__substr = 'Só mostra parte dunha cadea. A primeira opción é unha distancia para definir onde comeza a saída de texto (por omisión, 0). A segunda opción é unha distancia cando texto se devolve. Se é vacio, volve todo o texto que resta. A terceira opción define que caracteres se engadirán á saída cando se devolve unha subcadea (Por omisión: ...).';$strTransformation_text_plain__external = 'SÓ EN LINUX: Inícia unha aplicación externa e envia-lle o campo de datos por meio do input padrón.  Devolve a saída padrón da aplicación. Por omisión é Tidy, para que resulte código HTML claro. Por razóns de seguranza, ten que editar manualmente o ficheirolibraries/transformations/text_plain__external.inc.php e insertar as ferramentas que quer permitir que funcionen. A primeira opción, polo tanto, é o número do programa que quer usar e a segunda opción son os parámetros do programa. O terceiro parámetro, se é 1, usará htmlspecialchars() para convertir a saída (Por omisión é 1). Un cuarto parámetro, se é 1, porá un NOWRAP na cela de contidos para que toda a saída se mostre sen reformatar (Por omisión é 1)';
$strTransformation_text_plain__unformatted = 'Mostra o código HTML como entidades HTML. Non se usa o HTML para formatar.';
$strTruncateQueries = 'Interrumpir as procuras mostradas';  
$strType = 'Tipo';

$strUncheckAll = 'Quitar-lles as marcas a todos';
$strUnique = 'Único';
$strUnselectAll = 'Non seleccionar nada';
$strUpdatePrivMessage = 'Acaba de actualizar os privilexios de %s.';
$strUpdateProfile = 'Actualizar o perfil:';
$strUpdateProfileMessage = 'Actualizouse o perfil.';
$strUpdateQuery = 'Actualizar a procura';
$strUsage = 'Uso';
$strUseBackquotes = 'Protexer os nomes das tabelas e dos campos con&nbsp;" ` "';
$strUseHostTable = 'Usar a tabela de Host';  
$strUseTables = 'Usar as tabelas';
$strUseTextField = 'Use campo de texto';
$strUser = 'Usuario';
$strUserAlreadyExists = 'O usuario %s xa existe';
$strUserEmpty = 'O nome do usuario está vacío!';
$strUserName = 'Nome do usuario';
$strUserNotFound = 'Non se atopou o usuario seleccionado na tabela de privilexios.';
$strUserOverview = 'Vista xeral do usuario';
$strUsers = 'Usuarios';
$strUsersDeleted = 'Os usuarios seleccionados elimináron-se sen problemas.';
$strUsersHavingAccessToDb = 'Utilizadores que teñen acceso a &quot;%s&quot;';

$strValidateSQL = 'Validar SQL';
$strValidatorError = 'Non foi posible iniciar o comprobador de SQL. Comprobe que ten instaladas todas as extensións de php tal e como se descrebe na %sdocumentación%s.';
$strValue = 'Valor';
$strVar = 'Variable';
$strViewDump = 'Ver o esquema do volcado da tabela';
$strViewDumpDB = 'Ver o esquema do volcado do banco de datos';

$strWebServerUploadDirectory = 'directorio de subida (upload) do servidor web';
$strWebServerUploadDirectoryError = 'Non se pode acceder ao directorio que designou para as subidas (upload)';
$strWelcome = 'Benvida/o a %s';
$strWildcard = 'comodín';
$strWithChecked = 'Todos os marcados';
$strWritingCommentNotPossible = 'Non é posible escreber o comentario';
$strWritingRelationNotPossible = 'Non é posible escreber a relación';
$strWrongUser = 'Usuario ou contrasinal errado. Acceso negado.';

$strXML = 'XML';

$strYes = 'Si';

$strZeroRemovesTheLimit = 'Nota: Se estas opcións se configuran como 0 (cero) elimina-se o limite.';
$strZip = 'comprimido no formato "zip"';

// To translate
$strSwitchToTable = 'Switch to copied table';  //to translate
$strTransformation_text_plain__external = 'LINUX ONLY: Launches an external application and feeds the fielddata via standard input. Returns standard output of the application. Default is Tidy, to pretty print HTML code. For security reasons, you have to manually edit the file libraries/transformations/text_plain__external.inc.php and insert the tools you allow to be run. The first option is then the number of the program you want to use and the second option are the parameters for the program. The third parameter, if set to 1 will convert the output using htmlspecialchars() (Default is 1). A fourth parameter, if set to 1 will put a NOWRAP to the content cell so that the whole output will be shown without reformatting (Default 1)';

$strCharset = 'Charset';  //to translate
?>
