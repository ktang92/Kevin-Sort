Sort
====
<strong>November 21st Release</strong>
Users can now set an optional flag to specify a sort of valid URLs, invalid URLs, or all URLs from the input file.
The command for running main.py with this new feature is shown below:

    $python main.py [--valid|--invalid] input-file output-file

When "--valid" flag is set, the program sorts only valid URLs in user's input-file. When "--invalid" flag is set, the
program sorts only invalid URLs in user's input-file. When neither of these flags are set, the program sorts all URLs
in user's input-file by the comparison described below.

An URL is considered valid if the original URL matches the normalized URL. We made this assumption to simplify what is
considered valid since the things needed to be considered in normalized form are fairly standard.The same cases we are addressing
considering whether a url is normalized are therefore the same things we address in its validity. We didnt want to address
very small issues that may be contained in a non normalized URL, which some people still accept as valid. We felt the issues
addressed in making sure a url is normal eliminates most of the odd things in a url that would make it invalid. 

This program normalizes URLs using url_normalized.py module implemented by Nikolai Panov. This is a fairly standard
normalized form that covers the cases we were most concerned with. It normalizes URLs using the following rules:

<ul>
  <li>Take care of IDN domains.
  <li>Convert the scheme and host to lower case.</li>
  <li>Capitalize letters in escape sequences.</li>
  <li>Decode percent-encoded octets of unreserved characters.</li>
  <li>Remove the default port.</li>
  <li>Remove dot-segments.</li>
  <li>Remove duplicate slashes.</li>
  <li>Remove the "?" when the query is empty.</li>
  <li>Use 'http' schema by default when appropriate.</li>
  <li>For schemes that define a default authority, use an empty authority if the default is desired.</li>
  <li>For schemes that define an empty path to be equivalent to a path of "/", use "/".</li>
  <li>All portions of the URI must be utf-8 encoded NFC from Unicode strings.</li>
</ul>

Therefore our defintion of when a URL is in  normalized form, is a URL that abides by the above rules. 
Our definition of a valid URL is one that abides by these rules as well.

When the users asks for all URLs, the provided sorting algorithms sort URLs first by their validity, 
where valid URLs come before invalid ones. Next, the algorithm sorts by strings of the normalized URLs. 
The <, >, and == will all be the default string operators since we are treating the URLs as strings. 
The output file will contain the original URL from input file sorted by these two criteria.

If the user asks for only valid or invalid URLs, the set of URLs will be filtered appropriately.
We will then sort on the normalized version of the URLs, just like above. These will use the standard
string operators for the string of the normalized URL.

<strong>November 8th Release</strong>
For this release we integrated TA feedback and added the sorting algorithms from team Full House. 
We now offer eight algorithms for the user to choose from (IF=Instafeed, FH=Full House):

<ul>
<li>Quicksort (IF) - Average O(nlogn). Worst case is O(n^2) however quicksort is in place, 
which saves memory and thus we feel it is of value to the customer</li>
<li>Mergersort (IF) - Worst case O(nlogn)</li>
<li>Bubblesort (IF) - Worst case O(n^2)</li>
<li>Radixsort - (IF) Worst case O(k*n), where k is the length of the longest string. If all strings are unique
then k is O(logn) and Radix sort becomes O(nlogn)</li>
<li>Heapsort (FH)</li>
<li>Radixsort (FH)</li>
<li>Mergesort (FH)</li>
<li>Selectionsort (FH)</li>
</ul>

Adding this extra sorting functionality drew our attention to the brittle nature of our main method. We believe
that we will be better able to change sorting algorithms if our main is decoupled from the algorithms, so we
abstracted the algorithm information to algorithms.py. This module creates a single list of algorithms from the two 
teams sets. Since the algorithms are in a list we can index them simply, main knows that it recieves the list in sorted
order and can send back an index specifying what algorithm to run.

When we need to add new algorithms we can modify algorithms.py and leave main completely unchanged.


<strong>November 1st Release</strong>

Team Instafeed's sorting project.

For this exercise we decided to split the work amongst ourselves by having one person assigned to each of the sort algorithms, one person assigned to the user interaction portion, and the rest distributed between the algorithms to help where needed. The algorithms that we decided to use for our program are mergesort, bubblesort, quicksort, and radixsort. We chose the first three sorts because we were familiar with them and they fulfilled the runtime constraint that we needed. Our choice in Radix sort was made for us as it is the only sort that comes close to O(n) when the input is of the correct format. 

Our usage instructions are relatively simple. The user simply needs to have an input file with the URLs that they wish to sort in the same directory as main.py. All other .py files that are in the repo should also be in this same directory. The user can then run the program from the command line by entering into the directory where main .py is located:

	$cd location/where/main.py

Once the user the is in this directory they simply need to run main with the command:

	$python main.py <input file> <output file>

The program will ask which sorting algorithm that the user would like to use and upon user input will execute on the given input file. This will produce an output file (specified by the user) with all of the URLs in sorted order. 

We tried to make the user experience as easy as possible by letting the user know if they entered in the start command incorrectly and throwing exceptions if they gave bad input at any point. The following is printed if the user invokes the program incorrectly:

	$Usage: python main.py input-file output-file

We also included a test file called sorttest.py, it can be run with “python sorttest.py”.

<strong>Algorithms</strong>

<ul>
<li>Quicksort - Average O(nlogn). Worst case is O(n^2) however quicksort is in place, 
which saves memory and thus we feel it is of value to the customer</li>
<li>Mergersort - Worst case O(nlogn)</li>
<li>Bubblesort - Worst case O(n^2)</li>
<li>Radixsort - Worst case O(k*n), where k is the length of the longest string. If all strings are unique
then k is O(logn) and Radix sort becomes O(nlogn)</li>
</ul>



