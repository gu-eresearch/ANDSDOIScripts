<?php

//*********************************************************************************************************//
//
//   ANDS DOI MINTING SCRIPT
//   This script will mint a new DOI based on the xml and landing page url provided
//   Requires xml and url variable passed via POST
//
//   Author:  Arve Solland, eResearch Services, Griffith University - a.solland@griffith.edu.au
//
//*********************************************************************************************************//

//Settings
$app_id = "YOUR_APP_ID_HERE"; //Your ANDS APP_ID string

// Get POST variables
$url = $_POST["url"]; // Url for the landing page of the object you are minting the DOI for
$xml = $_POST["xml"]; // Valid Datacite xml describing the object you are minting

if ( !isset($url)  ) {
    print "Variable 'url' not found.\n";
} else if ( !isset($xml) ) {
    print "Variable 'xml' not found.\n";
} else { 
    // define the call to the service
    $requestURI = "https://services.ands.org.au/home/dois/doi_mint.php?app_id=".$app_id."&url=".urlencode($url);

    // Execute call
    //print "Executing CURL call...\n";
    // use curl to connect and run the service and receive the response
    $newch = curl_init();
    curl_setopt($newch, CURLOPT_URL, $requestURI); 
    curl_setopt($newch, CURLOPT_RETURNTRANSFER, true); 
    curl_setopt($newch, CURLOPT_CUSTOMREQUEST, "POST"); 
    curl_setopt($newch, CURLOPT_POSTFIELDS,$xml);


    $result = curl_exec($newch); 
    $curlinfo = curl_getinfo($newch); 
    curl_close($newch);

    if( $result ) {
        $resultXML = $result; 
    }
    print $resultXML; 

} 

?>