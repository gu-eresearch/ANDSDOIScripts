<?php

//*********************************************************************************************************//
//
//   ANDS DOI UPDATE SCRIPT
//	 This script will update the landing page url of a given DOI
//   Requires DOI_id and url variable passed via POST
//
//   Author:  Arve Solland, eResearch Services, Griffith University - a.solland@griffith.edu.au
//
//*********************************************************************************************************//

//Settings
$app_id = "YOUR_APP_ID_HERE"; //Your ANDS APP_ID string

// Get POST variables
$url = $_POST["url"]; // Url for the landing page of the object you are updating
$DOI_id = $_POST["DOI_id"]; // Existing DOI

if ( !isset($url)  ) {
    print "Variable 'url' not found.\n";
} else if ( !isset($DOI_id) ) {
    print "Variable 'DOI_id' not found.\n";
} else { 
	// define the call to the service
	$requestURI = "https://services.ands.org.au/home/dois/doi_update.php?app_id=".$app_id."&doi=".$DOI_id."&url=".urlencode($url);

    // Execute call
    //print "Executing CURL call...\n";
    // use curl to connect and run the service and receive the response
    $newch = curl_init();
    curl_setopt($newch, CURLOPT_URL, $requestURI); 
    curl_setopt($newch, CURLOPT_RETURNTRANSFER, true); 
    curl_setopt($newch, CURLOPT_CUSTOMREQUEST, "POST"); 

    $result = curl_exec($newch); 
    $curlinfo = curl_getinfo($newch); 
    curl_close($newch);

    if( $result ) {
        $resultXML = $result; 
    }
    print $resultXML; 

} 

?>