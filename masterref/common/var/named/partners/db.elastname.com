; $Id: db.elastname,v 1.1 2003/08/13 17:03:17 root Exp $
$TTL 400
;$TTL 86400
@       IN      SOA     host1.lunarmedia.net. admin.lunarmedia.net. (
                                2002052302      ; Serial
                                10800           ; Refresh after 3 hours
                                3600            ; Retry after 1 hour
                                604800          ; Expire after 1 week
;                                86400 )        ; Minimum TTL of 1 day
                                40 )    ; Minimum TTL of 1 day
 
                IN      NS      ns1.lunarmedia.net.
                IN      NS      ns2.lunarmedia.net.
 
                IN      A       12.237.81.250
 
www             IN      A       12.237.81.250
  
@               IN      MX 10   host1.lunarmedia.net.
