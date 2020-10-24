CREATE DATABASE Ecommerce;

CREATE TABLE Products (
    ID INT GENERATED ALWAYS AS IDENTITY,
    Name varchar(255) NOT NULL,
    ItemNumber varchar(30) NOT NULL,
    ShortDescription varchar(1000),
    ImageUrl varchar(200) NOT NULL,
--     TODO make a price, availability and unit of measure table to make this example more realistic
    Quantity int DEFAULT 0,
    Price float DEFAULT 0.00
);

-- Using RoundUp products as an example
INSERT INTO Products (ID,NAME,ItemNumber,ShortDescription,ImageUrl,Quantity,Price)
VALUES (1,
'Roundup® Landscape Weed Preventer',
4385118,
'Don''t Pull Weeds and Grasses, Prevent Them! Introducing Roundup® Landscape Weed Preventer which prevents weeds and grasses for up to 6 months, Guaranteed!* It works by forming a weed barrier to stop weeds before they start. For best results, apply directly to soil around plants in Spring before weeds germinate and before mulching. Won''t harm your desirable plants and flowers when used as directed! The easy to use built-in applicator provides even coverage. Now you can save time and energy with Roundup® Landscape Weed Preventer. A simple step towards a weed free landscape and garden!',
'https://www.roundup.com/sites/g/files/oydgjc121/files/styles/scotts_product_image/public/asset_images/US-Roundup-Landscape-Weed-Preventer-Main-4385248-Xxl%28v2%29.png?itok=r9qfygLn',
10,
19.99);

INSERT INTO Products (ID,NAME,ItemNumber,ShortDescription,ImageUrl,Quantity,Price)
VALUES (2,
'Roundup® For Lawns3 Ready-to-Spray',
5008810,
'Roundup® For Lawns3 is a formula that kills weeds, not the lawn! It controls over 250 common lawn weeds, roots and all, and is especially effective on hard-to-kill weeds such as crabgrass, dandelion, clover and yellow nutsedge. The ready-to-spray applicator is great for broadcast application to your entire lawn and covers up to 5000 square feet. This fast acting formula starts killing on contact and kills weeds down to the root so they don''t come back. In addition, its rainproof in as little as 3 hours! Roundup® For Lawns3 is a simple step towards a beautiful, weed free lawn.',
'https://www.roundup.com/sites/g/files/oydgjc121/files/styles/scotts_product_image/public/asset_images/500881005_2.jpg?itok=loJ06pl1',
10,
23.99);

INSERT INTO Products (ID,NAME,ItemNumber,ShortDescription,ImageUrl,Quantity,Price)
VALUES (3,
'Roundup® Ready-To-Use Max Control 365 with Comfort Wand',
5000510,
'Roundup® Ready-To-Use Max Control 365 kills and prevents weeds for up to 12 months by creating an invisible barrier.  Not only does it kill visible weeds, it kills them down to the root, guaranteed!* Apply the no-mix formula with the Comfort Wand® with continuous spray and extended reach for no bending.  For use on driveways, patios, sidewalks, and gravel areas, Roundup® Ready-To-Use Max Control 365 is rainproof in 30 minutes with visible results in 12 hours.  Use Roundup® to kill weeds.  Fast. ',
'https://www.roundup.com/sites/g/files/oydgjc121/files/styles/scotts_product_image/public/asset_images/2019-09-18_10-56-02.png.1500x1500.png?itok=kVTmxJ0r',
10,
38.49);

INSERT INTO Products (ID,NAME,ItemNumber,ShortDescription,ImageUrl,Quantity,Price)
VALUES (4,
'Roundup® Ready-To-Use Extended Control Weed & Grass Killer Plus Weed Preventer II with Comfort Wand',
5101910,
'The dual-action formula of Roundup® Ready-To-Use Extended Control Weed & Grass Killer Plus Weed Preventer II with Comfort Wand® kills existing weeds and prevents new ones from growing for up to four months—and it kills them down to the root, guaranteed!* Plus, the Weed & Grass Killer can be used on driveways, sidewalks, patios, along fences, curbs, retaining walls, and edges of lawns, as well as on decorative rock or gravel areas. Use the extendable Comfort Wand® with continuous spray for more accuracy without bending over. Rainproof in 10 minutes with visible results in 3 hours, Roundup® works. Fast.',
'https://www.roundup.com/sites/g/files/oydgjc121/files/styles/scotts_product_image/public/asset_images/2019-09-18_10-56-02.png.1500x1500.png?itok=kVTmxJ0r',
10,
29.99);

INSERT INTO Products (ID,NAME,ItemNumber,ShortDescription,ImageUrl,Quantity,Price)
VALUES (5,
'Roundup® Weed & Grass Killer Super Concentrate',
5100710,
'The best Roundup® brand concentrate value. Kills weeds to the root so they don''t come back. Can be used to treat stumps and prevent regrowth. Rainproof protection in 30 minutes. Can be used in and around vegetable gardens and for treating large areas.',
'https://www.roundup.com/sites/g/files/oydgjc121/files/styles/scotts_product_image/public/asset_images/US-Roundup-Weed-And-Grass-Killer-Super-Concentrate-Main-5100720-Xxl.png?itok=uXFJH-pe',
10,
4.99);

-- confirm everything worked
SELECT * FROM Products;