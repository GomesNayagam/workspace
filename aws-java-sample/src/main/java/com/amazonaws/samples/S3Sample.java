/*
 * Copyright 2010-2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
package com.amazonaws.samples;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.HashSet;
import java.util.List;
import java.util.TimeZone;
import java.util.UUID;

import org.apache.commons.io.FilenameUtils;

import com.amazonaws.AmazonClientException;
import com.amazonaws.AmazonServiceException;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.Bucket;
import com.amazonaws.services.s3.model.GetObjectRequest;
import com.amazonaws.services.s3.model.ListObjectsRequest;
import com.amazonaws.services.s3.model.ObjectListing;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.model.PutObjectRequest;
import com.amazonaws.services.s3.model.S3Object;
import com.amazonaws.services.s3.model.S3ObjectSummary;
import com.amazonaws.util.DateUtils;
import com.amazonaws.util.StringUtils;
import com.amazonaws.ClientConfiguration;
import com.amazonaws.Protocol;

/**
 * This sample demonstrates how to make basic requests to Amazon S3 using
 * the AWS SDK for Java.
 * <p>
 * <b>Prerequisites:</b> You must have a valid Amazon Web Services developer
 * account, and be signed up to use Amazon S3. For more information on
 * Amazon S3, see http://aws.amazon.com/s3.
 * <p>
 * <b>Important:</b> Be sure to fill in your AWS access credentials in the
 *                   AwsCredentials.properties file before you try to run this
 *                   sample.
 * http://aws.amazon.com/security-credentials
 */
public class S3Sample {

    public static void main(String[] args) throws IOException {
        /*
         * This credentials provider implementation loads your AWS credentials
         * from a properties file at the root of your classpath.
         *
         * Important: Be sure to fill in your AWS access credentials in the
         *            AwsCredentials.properties file before you try to run this
         *            sample.
         * http://aws.amazon.com/security-credentials
         */
    	
        /*AmazonS3 s3 = new AmazonS3Client(new ClasspathPropertiesFileCredentialsProvider());
        Region usWest2 = Region.getRegion(Regions.US_WEST_2);
        s3.setRegion(usWest2);*/

        String accessKey = "AKIAIBJ3TS7Q3CVZZNGQ";
        String secretKey = "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";

        AWSCredentials credentials = new BasicAWSCredentials(accessKey, secretKey);
        AmazonS3 conn = new AmazonS3Client(credentials);
        conn.setEndpoint("http://s3.amazonaws.com");
        
        
        String bucketName = "tataatsu_collablayerapp_dev";
        String key = "disquery";

        System.out.println("===========================================");
        System.out.println("Getting Started with Amazon S3");
        System.out.println("===========================================\n");

        HashSet<String> doc_type = new HashSet<String>();
        
        doc_type.add("png");
        doc_type.add("jpg");
        doc_type.add("doc");
        doc_type.add("pdf");
        
       // If-Modified-Since: Sun, 16 Mar 2014 18:30:00 GMT
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-mm-dd hh:mm:ss.S");
        String dateInString = "2014-03-17 09:30:51.377336";
        
        
        try {
			TimeZone gmtTime = TimeZone.getTimeZone("GMT");
			formatter.setTimeZone(gmtTime);
			Date dt = formatter.parse(dateInString);
			System.out.println(StringUtils.fromDate(dt));
			
			

			
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        
        
        try {
        	
        /*	List<Bucket> buckets = conn.listBuckets();
        	for (Bucket bucket : buckets) {
        	        System.out.println(bucket.getName() + "\t" +
        	                StringUtils.fromDate(bucket.getCreationDate()));
        	}
        	*/
        	
        	        	
/*               String ext = FilenameUtils.getExtension("query1/ramana.jpg");
               
               File temp = File.createTempFile(UUID.randomUUID().toString(), "." + ext);
               String tempFilePath = temp.getAbsolutePath();
               
               Date dt = new Date();
               Calendar c = Calendar.getInstance(); 
               c.setTime(dt); 
               c.add(Calendar.MINUTE, -10);
               dt = c.getTime();
               
               GetObjectRequest  req = new GetObjectRequest("disquery","query1/ramana.jpg");
               req.setModifiedSinceConstraint(dt);
               
              ObjectMetadata res  =  conn.getObject(
            	        req     ,
            	        new File(tempFilePath)
            	);
               
              if(res == null) temp.delete();
              
          	*/
        	
/*        	
        	ObjectListing objects = conn.listObjects("disquery");
       	
        	int i = 0;
        	
        	do {
    	        for (S3ObjectSummary objectSummary : objects.getObjectSummaries()) {
    	        	
    	        	 String ext = FilenameUtils.getExtension(objectSummary.getKey());
                     if (!(doc_type.contains(ext.toLowerCase()))){
                         continue;
                     }
    	        	    	        	
    	                System.out.println(i++ + ")" + objectSummary.getKey() + "\t" +
    	                		objectSummary.getSize() + "\t" +
    	                        StringUtils.fromDate(objectSummary.getLastModified()));
    	        }
    	        objects = conn.listNextBatchOfObjects(objects);
    	} while (objects.isTruncated());
        	
        	
*/
        	
        	
/*        	ListObjectsRequest listObjectsRequest = new ListObjectsRequest()
        	.withBucketName("disquery");
        	ObjectListing objectListing;
      	*/
        	/*do {
        		objectListing = conn.listObjects(listObjectsRequest);
        		for (S3ObjectSummary objectSummary : 
        			objectListing.getObjectSummaries()) {
        			System.out.println( " - " + objectSummary.getKey() + "  " +
        	                "(size = " + objectSummary.getSize() + 
        					")");
        		}
        		listObjectsRequest.setMarker(objectListing.getNextMarker());
        	} while (objectListing.isTruncated());
        	
        	*/
        	
        	
        	
        	
        	
/*        	  S3Object object = conn.getObject(new GetObjectRequest("disquery", "query1/st_zoo.sh"));
              System.out.println("Content-Type: "  + object.getObjectMetadata().getContentType());
              displayTextInputStream(object.getObjectContent());
        	*/
        	
        	System.out.println();
        	
        	/*
        	do {
        	        for (S3ObjectSummary objectSummary : objects.getObjectSummaries()) {
        	                System.out.println(objectSummary.getKey() + "\t" +
        	                        ObjectSummary.getSize() + "\t" +
        	                        StringUtils.fromDate(objectSummary.getLastModified()));
        	        }
        	        objects = conn.listNextBatchOfObjects(objects);
        	} while (objects.isTruncated());
*/
        	
            /*
             * Create a new S3 bucket - Amazon S3 bucket names are globally unique,
             * so once a bucket name has been taken by any user, you can't create
             * another bucket with that same name.
             *
             * You can optionally specify a location for your bucket if you want to
             * keep your data closer to your applications or users.
             */
        	
         /*   System.out.println("Creating bucket " + bucketName + "\n");
            s3.createBucket(bucketName);
          */
            /*
             * List the buckets in your account
             */
         /*   System.out.println("Listing buckets");
            for (Bucket bucket : s3.listBuckets()) {
                System.out.println(" - " + bucket.getName());
            }
            System.out.println();
*/
            /*tataatsu_collablayerapp_stg
             * Upload an object to your bucket - You can easily upload a file to
             * S3, or upload directly an InputStream if you know the length of
             * the data in the stream. You can also specify your own metadata
             * when uploading to S3, which allows you set a variety of options
             * like content-type and content-encoding, plus additional metadata
             * specific to your applications.
             */
       /*     System.out.println("Uploading a new object to S3 from a file\n");
            s3.putObject(new PutObjectRequest(bucketName, key, createSampleFile()));*/

            /*
             * Download an object - When you download an object, you get all of
             * the object's metadata and a stream from which to read the contents.
             * It's important to read the contents of the stream as quickly as
             * possibly since the data is streamed directly from Amazon S3 and your
             * network connection will remain open until you read all the data or
             * close the input stream.
             *
             * GetObjectRequest also supports several other options, including
             * conditional downloading of objects based on modification times,
             * ETags, and selectively downloading a range of an object.
             */
        	
 /*           System.out.println("Downloading an object");
            S3Object object = s3.getObject(new GetObjectRequest(bucketName, key));
            System.out.println("Content-Type: "  + object.getObjectMetadata().getContentType());
            displayTextInputStream(object.getObjectContent());
*/
            /*
             * List objects in your bucket by prefix - There are many options for
             * listing the objects in your bucket.  Keep in mind that buckets with
             * many objects might truncate their results when listing their objects,
             * so be sure to check if the returned object listing is truncated, and
             * use the AmazonS3.listNextBatchOfObjects(...) operation to retrieve
             * additional results.
             */
          /*  System.out.println("Listing objects");
            ObjectListing objectListing = s3.listObjects(new ListObjectsRequest()
                    .withBucketName(bucketName)
                    .withPrefix("di"));
            for (S3ObjectSummary objectSummary : objectListing.getObjectSummaries()) {
                System.out.println(" - " + objectSummary.getKey() + "  " +
                        "(size = " + objectSummary.getSize() + ")");
            }
            System.out.println();
*/
            /*
             * Delete an object - Unless versioning has been turned on for your bucket,
             * there is no way to undelete an object, so use caution when deleting objects.
             */
         /*   System.out.println("Deleting an object\n");
            s3.deleteObject(bucketName, key);
*/
            /*
             * Delete a bucket - A bucket must be completely empty before it can be
             * deleted, so remember to delete any objects from your buckets before
             * you try to delete them.
             */
           /* System.out.println("Deleting bucket " + bucketName + "\n");
            s3.deleteBucket(bucketName);*/
            
        } catch (AmazonServiceException ase) {
            System.out.println("Caught an AmazonServiceException, which means your request made it "
                    + "to Amazon S3, but was rejected with an error response for some reason.");
            System.out.println("Error Message:    " + ase.getMessage());
            System.out.println("HTTP Status Code: " + ase.getStatusCode());
            System.out.println("AWS Error Code:   " + ase.getErrorCode());
            System.out.println("Error Type:       " + ase.getErrorType());
            System.out.println("Request ID:       " + ase.getRequestId());
        } catch (AmazonClientException ace) {
            System.out.println("Caught an AmazonClientException, which means the client encountered "
                    + "a serious internal problem while trying to communicate with S3, "
                    + "such as not being able to access the network.");
            System.out.println("Error Message: " + ace.getMessage());
        }
    }

    /**
     * Creates a temporary file with text data to demonstrate uploading a file
     * to Amazon S3
     *
     * @return A newly created temporary file with text data.
     *
     * @throws IOException
     */
    private static File createSampleFile() throws IOException {
        File file = File.createTempFile("aws-java-sdk-", ".txt");
        file.deleteOnExit();

        Writer writer = new OutputStreamWriter(new FileOutputStream(file));
        writer.write("abcdefghijklmnopqrstuvwxyz\n");
        writer.write("01234567890112345678901234\n");
        writer.write("!@#$%^&*()-=[]{};':',.<>/?\n");
        writer.write("01234567890112345678901234\n");
        writer.write("abcdefghijklmnopqrstuvwxyz\n");
        writer.close();

        return file;
    }

    /**
     * Displays the contents of the specified input stream as text.
     *
     * @param input
     *            The input stream to display as text.
     *
     * @throws IOException
     */
    private static void displayTextInputStream(InputStream input) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(input));
        while (true) {
            String line = reader.readLine();
            if (line == null) break;

            System.out.println("    " + line);
        }
        System.out.println();
    }

}
