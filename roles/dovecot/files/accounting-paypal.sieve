require ["fileinto"];

if allof(
    address :is "from" "service@paypal.com",
    address :is "to" "friends@gnome.org"
) {
    fileinto "paypal-gnome";
    stop;
}

if allof(
    address :is "from" "service@paypal.com",
    address :is "to" "gimp@gnome.org"
) {
    fileinto "paypal-gimp";
    stop;
}
