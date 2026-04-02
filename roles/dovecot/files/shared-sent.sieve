require ["fileinto", "envelope", "subaddress"];

if envelope :detail "to" "sent" {
    fileinto "Sent";
    stop;
}
