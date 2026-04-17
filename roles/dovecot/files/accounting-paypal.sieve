require ["fileinto"];

if allof(
    address :is "from" "service@paypal.com",
    address :is "to" "friends@gnome.org"
) {
    fileinto "gnome-paypal";
    stop;
}

if allof(
    address :is "from" "service@paypal.com",
    address :is "to" "gimp@gnome.org"
) {
    fileinto "gimp-paypal";
    stop;
}
