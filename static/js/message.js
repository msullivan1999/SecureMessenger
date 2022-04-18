/*
* recipient_key is a string
* recipient is a string name
* nonce is a hex string [concat to the shared string]
*/

function get_params_and_send(recipient_key, recipient, nonce) {
	var msg = document.getElementById("message");
	var text = msg.value;
	var sender_public = sessionStorage.getItem('usr_key');
	var sender_priv = new Big( sessionStorage.getItem( sender_public ).toString() );
	var recipient_pub = new Big(recipient_key);
	var shared = recipient_pub.pow(parseInt(sender_priv)).mod(17);

	console.log(
		'recipient: ' + recipient +
		'\nsender:' + sessionStorage.getItem('current_user') + 
		"\nrecipient public: " + recipient_pub + 
		'\nsender public: ' + sender_public + 
		'\nsender private: ' + sender_priv
	);
	console.log(text);

	shared = parseInt(shared.toString());

	console.log(shared);

	// encrypt
	var ciphertext = CryptoJS.AES.encrypt(text.toString(), shared.toString() + nonce);

	console.log(ciphertext.toString()); // encrypts fine
	var decrypted = CryptoJS.AES.decrypt(ciphertext, shared.toString()+nonce);
	console.log(decrypted.toString(CryptoJS.enc.Utf8)); // decrypts fine

	// set ciphertext content to send back 2 da servr hehe ;)
	document.getElementById("ciphertext").value = ciphertext.toString();
	document.getElementById("sender_pub_key").value = sender_public.toString();
	document.getElementById("nonce").value = nonce;
	document.getElementById("recipient").value = recipient;
}
