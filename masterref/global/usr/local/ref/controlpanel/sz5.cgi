#!/usr/bin/perl -w

# $Id: sz5.cgi,v 1.2 2002/03/26 14:23:43 root Exp root $

use strict;
use Cwd;

my $workdir = `pwd`;
my @path = split(/\//, $workdir);
my $domain=$path[2];
my $rcs = (qw$Revision: 1.2 $)[-1];
my $images = "controlpanel/images";

$0 = (split(/\//, $0))[-1];
my $self = "controlpanel/$0";

### End of perl definitions ###

print<<START;
Content-type: text/html\n\n
<html>
<head>
    <title>
        Control Panel
    </title>
<SCRIPT LANGUAGE = "JavaScript"><!--
function startndnav(url) {
//alert (remoteWin);
   	remoteWin = window.open(url,'ndnav','toolbar=0,top=10,left=25,directories=0,status=0,menubar=0,scrollbars=no,resizable=no,width=394,height=450');
     remoteWin.location.href = url;
     	if (remoteWin.opener == null)     		
        remoteWin.opener = self;
     	if (window.focus)
     		remoteWin.focus();
     }

// -->
</SCRIPT>
<base href="https://www.$domain/">
</head>

<!-- BEGIN BODY DEFINES -->
   <body background="$images/portalback.gif" link="#000000" vlink="#000000" alink="#FFFF99" leftmargin="0" topmargin="0" marginheight="0" marginwidth="0"><img src="$images/trans10.gif" width="10" height="10" border="0" alt=""><br><img src="$images/trans10.gif" width="10" height="10" border="0" alt=""><br>
<!-- BEGIN TOP TABLE LINKS -->
   	<table width="693" border="0" cellspacing="0" cellpadding="0">
   		<tr><td><img src="$images/accountadministrationhead.gif" width="296" height="26" border="0" alt="Account Information"></td>
   			<td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><a href="javascript:window.close()">
<b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">LOG OUT</font></b></a><!--&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="">
<b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">FAQ</font></b>
</a>-->&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="mailto:support\@lunarhosting.net">
<b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">SUPPORT</font></b>
</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://www.$domain/controlpanel/">
<b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">HOME</font></b>
</a></font></td></tr>
   	</table>
   	<table border="0" cellspacing="0" cellpadding="0">
   		<tr><td><img src="$images/trans1.gif" width="2" height="1" border="0" alt=""><br><img src="$images/trans1.gif" width="2" height="1" border="0" alt=""></td></tr>
   	</table>
   	<table border="0" cellspacing="0" cellpadding="0"><tr><td width="193" valign="top" bgcolor="#CC3300">&nbsp;<p>
   			<center><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">Welcome!<br>www.$domain</font></center></div>	


<!--******* SIDE TOC *******-->
START
	
	require 'toc.lib';
	
print<<REST;
	
	<!--******* END TOC *******-->
<img src="$images/trans158.gif" width="1" height="195" border="0" alt=""><div align="center"><br><a href="http://www.lunarhosting.net/terms.htm"><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-2>Acceptable Usage Policy
</a><br><a href="http://www.lunarhosting.net/privacy.htm">Privacy Statement</a></font>
<p><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">Version: $rcs</font><p>
</div><img src="$images/trans158.gif" width="1" height="195" border="0" alt=""></font><br>
</td><td><img src="$images/trans10.gif" width="10" height="10" border="0" alt=""></td>
<td valign="top">
<table width="500" border="0" cellspacing="0" cellpadding="0">
<tr><td align="right"><a href="http://www.lunarhosting.net"><img src="$images/portalogo.gif"  border="0" alt="Lunar Media Inc."></a>&nbsp;<p></td>
</tr>
<tr>
<td>&nbsp;<p>

<!-- *********** -->   						              
<a name="top">
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>START SITE ADMINISTRATION </b><br>The administrative Web pages a
re located within a secure area. You should have been sent a URL to login to your Administration area.  You may want to bookmark thi
s page. <p> Please enter your user name and password. Your user name is always <b>admin</b>. You should have an email that was sent
you containing your administration password.<p>
<!-- MAIN TITLE -->
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>PRODUCTS</b>&nbsp; 
<!-- CATEGORY LINKS -->
<a href="$self#1">Viewing/Changing Product Details</a> | <a href="$self#2">Viewing/Changing Options</a> | <a href="$self#3">Add/Delete a Product</a>
<br>
<!-- MAIN BODY -->
Once logged into Admin, you will need to click on click on <b>STORE ADMIN</b> and then<b>PRODUCTS</b> link from the list of links on the left.  Once you get to this page, you should see a list off all the products in your store. If you would like to shorten the list of products, a quick way to do this is to do a search from the search menu. It doesn't have to be anything specific. You can then save the search by clicking on Save Search.  The next time you review your products, you will just see this search. To view all of your products, you simply click on <b>VIEW ALL PRODUCTS</b>.
<p>
Below is a tutorial on how to add/delete products from your store. It also will walk you through adding options and changing information on the products you currently have.  <b>This tutorial does not include information on uploading images to your site.</b> Please <a href="mailto:support\@lunarhosting.net"><b>email us</b></a> if you need assistance on uploading images.
<a name="1"><p><b>Viewing/Changing Product Details</b><br></a>
You can click on the link directly from the PRODUCT ADMINISTRATION PAGE. When making any changes, you must make the change and then click on the <b>UPDATE RECORD</b> button at the bottom of the page. If the change was successful, it will say "Record Updated"<p> Once you view a product, you will see a display of the product DETAILS:<br> 
<b>CATEGORY:</b> this is a menu that contains all the categories that are set up for your site currently. If you want to change the product into a different category, you can select a new option from the drop down menu. The category must have already been set up. You can not change category information from this area of administration. You must go to category administration, by clicking CATEGORIES on the left menu. <br>
<b>PART NUMBER: </b>This is a unique number that you establish to identitfy your product. You can name it however you would like.<br>
<b>PRODUCT NAME:</b> Enter the name of the Product here. You can NOT use custom HTML here.<br>
<b>SUMMARY:</b>This is a SHORT description of your product. It normally shows up on the page under the thumbnails, as well as, on the product detail.  You do NOT need to duplicate this text in the <b>DETAIL</b> text area of the product. You can NOT use custom HTML here.<br>
<b>DETAIL:</b>You can add text here to go into your product detail page. You can add custom HTML here.  Here are the basic HTML tags you need to put in your code if you would like to format the text.
<table border="0" cellspacing="0" cellpadding="5"><tr><td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1">&nbsp;&nbsp;<b>&lt;br&gt; </b>BREAK TAG.  Put this after the end of a sentence if you want it to go to the next line.<br>
&nbsp;&nbsp;<b>&lt;p&gt;</b> PARAGRAPH TAG. Put this tag at the end of a sentence you want a paragraph break to be used.<br>
&nbsp;&nbsp;<b>&lt;b&gt; and &lt;/b&gt; </b>BOLD tags.  This tag allows you to bold a word or group of words. You must put the text you want bolded between these tags. The first tag states you want to begin bolding, and the last tag states you want to end bolding.  So, the way to edit the code is to &lt;b&gt; <b>PUT THE TEXT HERE</b> &lt;/b&gt;</font></td></tr></table>
There are many other HTML tags available to use, however, these are the most common.<br>
<b>PRICE:</b> Enter the price here. Do not use the \$ sign.
<b>IMAGE and THUMBNAIL:</b> If the image is on our server, you can select the CHANGE IMAGE button and navigate to the image.  You may also type the exact name of the image. Please be aware that this information is case sensitive.<br>
<b>SHIPPING WEIGHT:</b> If your shipping is calculated by weight, enter the ammount here. If you do not depend on weight, you should leave this field at 0.00.
<b>INVENTORY:</b> If you want to keep track of your internet inventory, you can add in the number you currently have of this product. Each time someone purchases a product, this number will decrease.  If you do not want to track inventory, leave this number at 0.<br>
<b>RE-ORDER QUANTITY:</b> If you are tracking inventory, you can enter a number here that you wish to get a re-order reminder. Once the inventory gets to this number an email will be sent to you telling you when you need to re-order. Leave this number at 0 if you are not tracking Inventory.<br>
<b>SEQUENCE NUMBER:</b> If you want your products to be displayed in a specific order, you must number them from this area. Default is listed in alpahbetical order.  Leave it at 0 if you do not plan on using this feature.<br>
<b>SHIPPING SURCHARGE:</b> If you have a special charge you want to add for a particular item, you add it here. It will be calculated per product they purchase.<p><font face="verdana,arial" color="#ffffcc" size="1"><a href="$self#top">back
          to the top</a></font><p>
<a name="2"><b>Viewing/Changing Options</b><br>
You can also display specific OPTIONS for your product. These are customized to how you want them displayed. To view these options, choose <b>List options for this product</b>.
If you have no options for this product, it will display '0 found' when you click on this link. Otherwise, you will see a list of the options you have set up for your product.  Click on the option you wish to change. WARNING: Be careful not to click "DELETE". It will delete this option, and there is no way to undo this.<br>
<b>PRODUCT ID:</b> This is different from your PART NUMBER. This is a number that ShopZone assigns to your product. Leave this entry as is.<br>
<b>OPTION NAME:</b> This is the text that will be displayed on the product detail page. If you want the options to go in a specific order, it is a good idea to number them. Default is to be listed alphabetically. This keeps them in the right order.<br>
<b>FORMAT:</b>You can choose <b>Radio</b> Format if you want the person to only select on of a series of options. For example, Red- Green- Blue-, and they can only select one color.  <b>Listbox</b> is needed, if you want a longer list of selections, and want only one selection to be chosen. This has a small arrow that once a user clicks on it, it drops down and can scroll up or down. <b>Checkbox</b> is available if you want a usuer to select more than one selection, or allow them to uncheck the box if they decide to. This is a good format to use if you are listing more than separate options. <b>Text</b> is used if you require a user to fill in some sort of information. For example, a user wants to add a personal message to a gift card.  They would enter this in here.  
<b>VALUES:</b> Enter the values here if you wish to offer different selections. For example, Red on one line, Green on another.<br>
<b>PRICE ADUSTMENTS:</b> <i><b>Please discuss this with us if you do not wish this to be displayed next to the option.</b></i> If you have a price difference of $1.00 if someone selects this option, you enter it here. Leave it blank if you do not wish to add additional costs for this option. <p>
Remember, options must be set up for each product you want to offer these options on. You can add as many as you wish to add.<br>
<font face="verdana,arial" color="#ffffcc" size="1"><a href="$self#top">back
          to the top</a></font><p>
<a name="3"><b>Add/Delete a Product</b><br>
<b>ADD PRODUCT</b><br>
From the PRODUCT ADMINISTRATION page, you can add a new product by clicking on the <b>"Add new product"</b> link at the bottom of the list of products. Enter all the information in each of the fields. Please refer to the above section for a description of each field.  If you wish to add an image, please make sure you have it on the server. <b> There is a current "bug" in ShopZone that requires you to add all the product information in except the product image and thumbnail. After you add the product, you must  then go back in and enter the information on the image and thumbnail for the product. Then you click "update product". It should then go through. If you have problems with this, please contact us.</b><P>
<b>OPTIONS</b><br>
To add a product option, you must first enter all the information on the product as described above. Once the product has been added,  simply click on "Add options for this product". Then add the information in as described in the above section. Make sure to click <b>ADD RECORD</b> after you add the option information.<p>
<b>DELETE PRODUCT</b><br>
To delete a product, you can do it one of a few ways. You can delete directly from the first PRODUCT ADMINISTRATION page. You can delete multiple products by checking the checkbox next to the product name on this page and then clicking on "Delete Checked Items". You can delete from the PRODUCT DETAIL page by choosing Delete, next to the View Link..
<p><font face="verdana,arial" color="#ffffcc" size="1"><a href="$self#top">back
          to the top</a></font><p>                            

   						</td>
   					</tr>
   				</table>
   			</td>
   		</tr>
   	</table>
   </body>
</html>
REST
