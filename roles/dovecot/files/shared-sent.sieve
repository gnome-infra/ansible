require ["fileinto", "envelope", "subaddress", "variables"];

if anyof(
    envelope :detail "to" "sent",
    envelope :matches "to" "*+sent@*"
) {
    fileinto "Sent";
    stop;
}
