Miva Empresa (Virtual Machine) v4.00, README.txt
$Id: README-vm.txt,v 1.4 2002/07/25 21:59:40 tracy Exp $

Thank you for downloading this release version of Miva Empresa (Virtual Machine).

CONFIGURATION AND INSTALLATION
------------------------------
The Miva Virtual Machine for UNIX is a cgi-bin application that is designed to
be executed by a webserver, such as Apache or Zeus.  Installation is fairly
simple and anyone who has installed a previous version of the Miva Engine
should have no difficulty.

The configuration system in the Miva Virtual Machine has been modularized, so
that hosting providers with custom provisioning systems can develop custom
configuration engines.  A configuration library is a DSO that is loaded by the
Miva Virtual Machine and then queried for configuration values.

This release of the Miva Virtual Machine ships with two configuration
libraries: "lib/config/3x.so" and "lib/config/env.so".  "3x.so" is a
configuration library that provides compatibility with the configuration file
used by v3.x of Miva Empresa.  "env.so" is a configuration library that
obtains configuration values from environment variables.

The Miva Virtual Machine first looks for its configuration library as
"libmivaconfig.so" in the current directory.  If this file is not found,
then the engine tries to load the DSO identified by the environment variable
MvCONFIG_LIBRARY (if set).  For security reasons, the owner of the
configuration library must be either the same as the user executing the Miva
Virtual Machine, or root.

STEP BY STEP APACHE INSTALLATION
--------------------------------
1. Place the file "cgi-bin/mivavm" in your Apache "cgi-bin" directory.

2. Change the ownership and permissions of the "mivavm" binary with the
   following commands:

	# chown root.root mivavm
	# chmod 4755 mivavm

3. Add the following lines to your "httpd.conf" (or "srm.conf", if using
   an older version of Apache).

	SetEnv MvCONFIG_LIBRARY /usr/local/miva/lib/config/env.so
	SetEnv MvCONFIG_DIR_MIVA /home/httpd/html
	SetEnv MvCONFIG_DIR_DATA /home/httpd/mivadata
	SetEnv MvCONFIG_DIR_BUILTIN /usr/local/miva/lib/builtins

	AddType application/x-miva-compiled .mvc
	Action application/x-miva-compiled /cgi-bin/mivavm

   The above lines assume that you have extracted the Miva Virtual Machine
   distribution file into /usr/local/miva, and that your Apache DocumentRoot
   is /home/httpd/html

4. You may override any Miva Virtual Machine configuration directives for a
   Virtual Host by placing "SetEnv MvCONFIG_..." directives inside the
   <VirtualHost> block.

5. Restart your Apache server.

CONFIGURATION REFERENCE - 3x.so
-------------------------------
For the most part, 3x.so behaves identically to the Miva Empresa 3.x
configuration.  As such, you may refer to the UNIX Empresa configuration
documentation on the Miva website for additional information.

The following additional configuration tags are supported:

<BUILTIN-LIB LIBRARY="path">
		
		Register the builtin function library <LIBRARY>.

<DATABASE-LIB METHOD="type" LIBRARY="path">

		Register the database library <LIBRARY> with database type <METHOD>.

CONFIGURATION REFERENCE - env.so
--------------------------------
env.so loads configuration values from environment variables.  Please
note that the names of the environment variables are case sensitive.

Environment Variable		Description
----------------------------------------------------------------------
MvCONFIG_DIR_MIVA			Root directory for .mvc files
MvCONFIG_DIR_DATA			Root data directory
MvCONFIG_DIR_CA				Directory containing SSL certificate files
MvCONFIG_DIR_USER			Analagous to Apache "UserDir" directive
MvCONFIG_DIR_USERDATA			Identical to 3.x "authuserdir" setting
MvCONFIG_INFO_SERVERADMIN	Email address of server administrator
MvCONFIG_SSL_OPENSSL		Full path to libssl.so (if available)
MvCONFIG_SSL_CRYPTO			Full path to libcrypto.so (if available)
MvCONFIG_TIMEOUT_GLOBAL		Global application timeout (seconds)
MvCONFIG_TIMEOUT_MAIL		MvPOP/MvSMTP network timeout (seconds)
MvCONFIG_TIMEOUT_CALL		MvCALL network timeout (seconds)
MvCONFIG_COOKIES			Output htscallerid cookie (boolean)
MvCONFIG_FLAGS_SECURITY		Identical to 3.x "securityoptions" setting

env.so automatically loads all .so files contained in the directory
specified by the environment variable MvCONFIG_DIR_BUILTIN (if specified).

To register a commerce library or database library, create an environment
variable with the name in the following form:

	MvCONFIG_DATABASE_<method>
	MvCONFIG_COMMERCE_<method>

Where <method> is the desired commerce method or database type.  The value of
this environment variable should be the full path to the library file.
