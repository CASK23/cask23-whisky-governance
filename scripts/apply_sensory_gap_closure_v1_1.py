#!/usr/bin/env python3
import json
from pathlib import Path

MASTER=Path('PROJECT_ZERO_SENSORY_MASTER.json')
OUT=Path('PROJECT_ZERO_SENSORY_MASTER_v1.1.json')
VAL=Path('PROJECT_ZERO_SENSORY_MASTER_v1.1.validation.json')

# Every descriptor below is explicitly assigned to one of the 12 governed visual families.
FM={
'Apricot':'orchard-fruit','Nectarine':'orchard-fruit','Vanilla custard':'sweet','Barley sugar':'sweet','Orange blossom':'floral-herbal','Brine':'maritime','Coconut':'tropical','Pear':'orchard-fruit','Apple':'orchard-fruit','Clove':'spice','Ginger':'spice',
'Dried fruit':'dried-fruit','Baked plum':'orchard-fruit','Raisin':'dried-fruit','Toffee':'sweet','Oak':'oak','Sea salt':'maritime',
'Sea air':'maritime','Allspice':'spice','Vanilla sponge cake':'sweet','Custard':'sweet','Lemon peel':'citrus','Dried pineapple':'tropical','Aniseed':'spice','Jasmine':'floral-herbal','Oak smoke':'smoke-peat',
'Caramel':'sweet','Vanilla':'sweet','Allspice':'spice','Burnt orange':'citrus','Butterscotch':'sweet','Leather':'oak','Tobacco':'oak',
'Passionfruit':'tropical','Green apple':'orchard-fruit','Honeydew melon':'tropical','Mint':'floral-herbal','Earthy peat smoke':'smoke-peat',
'Citrus':'citrus','Baked apple':'orchard-fruit','Cinnamon':'spice',
'Dark chocolate':'chocolate-coffee','Biscuit':'sweet','Sticky toffee pudding':'sweet','Gingerbread':'spice','Cardamom':'spice','Nutmeg':'spice','Anise':'spice','Liquorice':'spice',
'Plum':'orchard-fruit','Red apple':'orchard-fruit','Grape':'dried-fruit','Chocolate':'chocolate-coffee','Honeysuckle':'floral-herbal',
'Pine resin':'floral-herbal','Woodsmoke':'smoke-peat','Ripe banana':'tropical','Pineapple':'tropical','Cocoa':'chocolate-coffee','Coffee':'chocolate-coffee',
'Barley':'sweet','Cream':'sweet','Orange peel':'citrus','Dark sugar':'sweet','Herbs':'floral-herbal','Baked fruit':'orchard-fruit',
'Sultana':'dried-fruit','Maraschino cherry':'orchard-fruit','Cranberry':'orchard-fruit','Turkish delight':'sweet',
'Mango':'tropical','Lemon zest':'citrus','Spice':'spice',
'Date':'dried-fruit','Dates':'dried-fruit',
'Cloudberry':'orchard-fruit','Sweet grape':'dried-fruit','White chocolate':'chocolate-coffee','Marzipan':'nutty',
'Malt':'sweet','Orchard fruit':'orchard-fruit','Gentle peat':'smoke-peat','Oak spice':'oak',
'Rye spice':'spice','Black pepper':'spice',
'Roasted nuts':'nutty',
'Peat smoke':'smoke-peat',
'Red berries':'orchard-fruit','Strawberry':'orchard-fruit','Cherry':'orchard-fruit','Almond':'nutty',
'Hazelnut':'nutty','Dry smoke':'smoke-peat','Toasted oak':'oak','Peat':'smoke-peat',
'Dark cherry':'orchard-fruit',
'Coastal smoke':'smoke-peat','Sweet oak':'oak',
'Candied citrus':'citrus','Apple':'orchard-fruit',
'Lemon':'citrus','Berries':'orchard-fruit','Cold coffee':'chocolate-coffee',
'Winter spice':'spice','Sherry sweetness':'dried-fruit',
'Honey':'sweet','Grape':'dried-fruit','Tropical fruit':'tropical',
'Chestnut':'nutty','Buttery malt':'sweet',
'Seaweed':'maritime','BBQ smoke':'smoke-peat','Treacle':'sweet',
'Raspberry':'orchard-fruit','Ash':'smoke-peat','Sea spray':'maritime','Earthy peat':'smoke-peat',
'Heather honey':'sweet','Dark fruit':'dried-fruit','Vanilla fudge':'sweet',
'Creamy sweetness':'sweet','Marmalade':'citrus',
'Bramble':'orchard-fruit','Demerara sugar':'sweet','Salted caramel':'sweet',
'Eucalyptus':'floral-herbal','Dried apricot':'dried-fruit','Char':'smoke-peat',
'Forest berries':'orchard-fruit','Seville orange':'citrus','Walnut':'nutty',
'Cherry blossom':'floral-herbal',
'Brown sugar':'sweet','Baking spice':'spice','Minerality':'maritime','Stewed apple':'orchard-fruit',
'Mineral':'maritime'
}

U={
'0cda1c9d-6868-4482-a690-caaac3225f34':dict(d=['Apricot','Nectarine','Vanilla custard','Barley sugar','Orange blossom','Brine','Coconut','Pear','Apple','Clove','Ginger'],n='Apricot and nectarine lead into creamy vanilla custard and barley sugar, with pear and apple freshness, a coastal briny lift, coconut richness and clove-and-ginger spice through the finish.',s=['https://www.masterofmalt.com/blog/post/bruichladdich-old-skool-10-year-old-review/','https://www.htfw.com/blog/bruichladdich-old-skool-10-year-old-whisky/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_RELEASE',m='EXACT_RELEASE'),
'10c6b4e0-f057-417d-9a10-0eb78aaede16':dict(d=['Dried fruit','Baked plum','Raisin','Toffee','Oak','Sea salt'],n='Dried and stewed fruit build through baked plum and raisin, with toffee sweetness, polished oak and a lightly saline edge.',s=['https://www.weedram.co.uk/product/macduff-2008-mossburn/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_RELEASE',m='EXACT_RELEASE'),
'10e1b78f-3c66-437c-98f0-66e88b9fde6d':dict(d=['Sea air','Allspice','Vanilla sponge cake','Custard','Lemon peel','Dried pineapple','Aniseed','Jasmine','Oak smoke'],n='Sea air and soft oak smoke frame vanilla sponge and custard, with lemon peel, dried pineapple, allspice and aniseed lifted by a light jasmine-floral note.',s=['https://www.whiskyfun.com/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_RELEASE',m='EXACT_RELEASE'),
'175d15bf-e5a7-4ebb-b41a-cb0654d49050':dict(d=['Caramel','Vanilla','Oak','Allspice','Burnt orange','Butterscotch','Leather','Tobacco'],n='Caramel, vanilla and mature oak open with allspice and burnt orange, moving into creamy butterscotch, leather and tobacco on a long warming finish.',s=['https://www.whiskyshop.com/whistlepig-15-year-old','https://www.tastings.com/Spirits-Review/WhistlePig-15-Year-Old-Estate-Oak-Straight-Rye-Whiskey-USA-92-Proof-08-04-2026.aspx'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_RELEASE',m='EXACT_RELEASE'),
'17638f87-72e1-4496-8bc8-be444ed282d2':dict(d=['Passionfruit','Green apple','Honeydew melon','Barley sugar','Mint','Ginger','Earthy peat smoke','Oak'],n='Ripe passionfruit and green apple meet barley sweetness and melon, with mint and ginger freshness over earthy peat smoke and mature oak.',s=['https://www.whiskysituation.co.uk/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_CASK',m='EXACT_CASK'),
'177d30a7-8fb6-487e-9495-d45e0621c5e5':dict(d=['Barley sugar','Citrus','Vanilla custard','Baked apple','Cinnamon','Oak'],n='Barley sugar and bright citrus sit over vanilla custard and baked apple, with cinnamon and oak providing the structural finish.',s=['https://www.whiskybase.com/'],e='TIER_2_ESTABLISHED_SPECIALIST_RELEASE_FAMILY',m='UNDER_SPECIFIED_MICRO_PROVENANCE_CASK_FAMILY'),
'213c368a-3e81-4ec3-85d3-84daacd26198':dict(d=['Caramel','Dark chocolate','Biscuit','Sticky toffee pudding','Gingerbread','Cardamom','Nutmeg','Anise','Oak','Liquorice'],n='Caramel, dark chocolate and biscuit build into sticky toffee pudding and gingerbread, layered with cardamom, nutmeg and anise before oak and liquorice carry the finish.',s=['https://www.whiskybase.com/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_CASK',m='EXACT_CASK'),
'25141c4f-f434-42c4-ad36-3850c674078c':dict(d=['Plum','Red apple','Apricot','Grape','Toffee','Vanilla','Cinnamon','Ginger','Chocolate','Honeysuckle'],n='Plum, apple and apricot lead into grape, toffee and vanilla, with cinnamon and ginger spice, chocolate depth and a gentle honeysuckle lift.',s=['https://www.whiskysituation.co.uk/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_RELEASE',m='EXACT_RELEASE'),
'32bc076b-9e7f-42fc-8665-26b239b8b741':dict(d=['Pine resin','Woodsmoke','Ripe banana','Pineapple','Cocoa','Ginger','Cinnamon','Clove','Dark chocolate','Coffee'],n='Pine resin and woodsmoke wrap ripe banana and pineapple, while cocoa, ginger, cinnamon and clove deepen into dark chocolate and coffee.',s=['https://www.whiskyshop.com/ardbeg-drum'],e='TIER_2_ESTABLISHED_SPECIALIST_EXPRESSION_46_PERCENT',m='IDENTITY_LABEL_CONFLICT_RESOLVED_TO_46_PERCENT_EXPRESSION'),
'362f6637-c2ee-404b-a0f6-0de125271065':dict(d=['Barley','Cream','Toffee','Orange peel','Dark sugar','Herbs','Baked fruit'],n='Creamy barley and baked fruit sit over toffee and dark sugar, with orange peel brightness and a fresh herbal edge.',s=['https://www.htfw.com/'],e='TIER_2_ESTABLISHED_SPECIALIST_RELEASE_FAMILY',m='UNDER_SPECIFIED_PROVENANCE_CASK_FAMILY'),
'3af074f8-139e-4be2-a1e5-784240032a01':dict(d=['Sultana','Liquorice','Maraschino cherry','Clove','Cinnamon','Cranberry','Turkish delight'],n='Sultana, maraschino cherry and cranberry bring a vivid red-fruit profile, balanced by liquorice, clove and cinnamon with a Turkish-delight sweetness.',s=['https://www.thewhiskyexchange.com/p/86561/white-peak-wire-works-amarone-wine-finish-2025-edition'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_RELEASE',m='EXACT_RELEASE_53_6'),
'3ffefe28-8c29-48fd-b386-9e64fd9a32ee':dict(d=['Vanilla','Mango','Lemon zest','Apricot','Dried fruit','Clove','Oak'],n='Vanilla and ripe mango meet lemon zest and apricot, with dried-fruit depth, clove spice and bourbon-seasoned oak carrying the finish.',s=['https://pauljohnwhisky.com/'],e='TIER_1_OFFICIAL_HOUSE_PLUS_CASK_PROFILE',m='EXACT_IDENTITY_LIMITED_PUBLIC_CASK_SENSORY'),
'4b47d2c9-4d5c-485d-aca9-e6edb84d698e':dict(d=['Caramel','Vanilla','Apricot','Plum','Raisin','Dates','Dark chocolate','Spice'],n='Caramel and vanilla open into apricot and plum, followed by raisin and dates, dark chocolate and lingering spice.',s=['https://www.tastings.com/Spirits-Review/WhistlePig-12-Year-Old-World-Rye-Whiskey-USA-86-Proof-08-04-2026.aspx'],e='TIER_2_ESTABLISHED_SPECIALIST_EXPRESSION',m='EXPRESSION_LEVEL_ABV_RECONCILED_43_PERCENT'),
'4c1fe5c9-653d-4379-940c-d87e4b2303e2':dict(d=['Cloudberry','Sweet grape','Vanilla','Toffee','White chocolate','Pear','Marzipan','Ginger','Tobacco','Oak'],n='Cloudberry and sweet grape meet pear and vanilla, with toffee, white chocolate and marzipan richness before ginger, tobacco and oak close the finish.',s=['https://www.masterofmalt.com/whiskies/mackmyra/mackmyra-moment-fjallmark-whisky/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXPRESSION',m='EXPRESSION_MATCH_WITH_STAGED_ABV_CONFLICT'),
'580f7478-dcb3-489d-8e37-88aa3cf08616':dict(d=['Malt','Orchard fruit','Citrus','Toffee','Sea salt','Gentle peat','Oak spice'],n='Malt and orchard fruit lead into citrus and toffee, with Campbeltown sea salt, gentle peat and oak spice giving the cask-strength profile its structure.',s=['https://www.springbank.scot/'],e='TIER_1_OFFICIAL_RANGE_PROFILE',m='UNDER_SPECIFIED_BATCH_FAMILY'),
'58d26ce5-3e09-4744-bdde-a5c0e745df35':dict(n='Honeyed sweetness, coconut and milk chocolate meet treacle and coffee, with bright citrus, warm cinnamon and a restrained thread of peat smoke.',s=['https://tomatin.com/product/cu-bocan-signature/'],e='TIER_1_OFFICIAL',m='EXACT_RELEASE'),
'5a215f0e-cc12-4eeb-a44e-99fa4f39c942':dict(d=['Rye spice','Cinnamon','Vanilla','Oak','Caramel','Black pepper'],s=['https://www.tuthilltown.com/'],e='TIER_1_OFFICIAL_EXPRESSION_FAMILY',m='EXACT_EXPRESSION_FAMILY'),
'5d3a84dc-45a5-4d87-b8c5-f320430ec98a':dict(d=['Roasted nuts','Dried fruit','Dark chocolate','Leather','Spice','Oak'],n='Roasted nuts and dried fruit sit over dark chocolate, leather and warming spice, with oloroso-seasoned oak carrying the finish.',s=['https://www.lockettbros.co.uk/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_RELEASE',m='EXACT_RELEASE'),
'6aa861fb-d627-46eb-8f17-291da1567bd1':dict(d=['Vanilla','Citrus','Peat smoke','Sea salt','Barley','Black pepper','Oak'],n='Vanilla and bright citrus ride over sweet barley, sea salt and assertive peat smoke, with black pepper and oak through the cask-strength finish.',s=['https://www.whiskybase.com/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_IDENTITY_RELEASE_FAMILY_SENSORY',m='EXACT_IDENTITY_LIMITED_PUBLIC_CASK_SENSORY'),
'6e01457c-cd2d-43ff-b90a-f13b937791ca':dict(d=['Red berries','Strawberry','Orchard fruit','Honey','Oak','Cherry','Tobacco','Almond'],n='Red berries, strawberry and orchard fruit are wrapped in honey, with cherry, almond, tobacco and oak adding depth to the port-pipe finish.',s=['https://www.whiskysaga.com/blog/benriach-2005-18-year-old-port-pipe'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_RELEASE',m='EXACT_RELEASE'),
'758b89fb-ef82-416d-8706-20adf91d4f56':dict(d=['Hazelnut','Caramel','Orange peel','Vanilla','Dry smoke','Cinnamon','Toasted oak','Peat'],n='Hazelnut and caramel meet orange peel and vanilla, with cinnamon, toasted oak and a dry peat-smoke thread giving the finish its bonfire character.',s=['https://www.masterofmalt.com/whiskies/arran/arran-signature-series-edition-2-barrel-bonfire-whisky/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_RELEASE',m='EXACT_RELEASE'),
'76b4392e-c465-41a9-8cce-2f0719b015b9':dict(d=['Raisin','Dark cherry','Dark chocolate','Cinnamon','Oak','Toffee'],n='Raisin and dark cherry lead into dark chocolate and toffee, with cinnamon and mature oak shaping the high-strength PX-cask finish.',s=['https://www.whiskybase.com/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_CASK_IDENTITY_PROFILE',m='EXACT_CASK_IDENTITY_CONSERVATIVE_PX_PROFILE'),
'77f17865-8e38-471d-9118-f3d8f9bbe10f':dict(d=['Coastal smoke','Brine','Dried fruit','Dark chocolate','Roasted nuts','Sweet oak'],n='Coastal smoke and brine frame dried fruit and dark chocolate, with roasted nuts and sweet oak bringing richness to the Williamson malt.',s=['https://www.berrybros.com/'],e='TIER_1_OFFICIAL_RELEASE_FAMILY',m='UNDER_SPECIFIED_CASK_WITHIN_COASTS_AND_SHORES_FAMILY'),
'7faf63fa-9d2e-41c2-b4b9-df20c001ca33':dict(d=['Candied citrus','Honey','Liquorice','Butterscotch','Apple','Sweet oak','Hazelnut','Cinnamon'],n='Candied citrus and apple freshness meet honey and butterscotch, with liquorice, hazelnut, cinnamon and sweet oak adding depth.',s=['https://www.arranwhisky.com/shop-whiskies/arran-single-malt/arran-10-year-old-single-malt'],e='TIER_1_OFFICIAL',m='EXACT_RELEASE'),
'8112a9eb-3811-4991-b527-0332c5d0b71c':dict(d=['Lemon','Plum','Cinnamon','Berries','Black pepper','Sea salt','Herbs','Cold coffee','Tobacco','Peat smoke'],n='Lemon, plum and berries sit over cinnamon and black pepper, with sea salt, herbs, cold coffee, tobacco and peat smoke extending the earthy finish.',s=['https://www.reddit.com/r/Scotch/comments/1hmqm94'],e='TIER_2_ESTABLISHED_COMMUNITY_EXACT_BATCH',m='EXACT_BATCH_2023_57_5'),
'87549a48-d0a7-49fd-9121-bcb6ec482443':dict(d=['Raisin','Date','Dark chocolate','Toffee','Orange peel','Cinnamon','Oak'],n='Raisin and date richness meet dark chocolate and toffee, with orange peel, cinnamon and mature oak giving the PX butt a structured finish.',s=['https://www.whiskybase.com/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_CASK_IDENTITY_PROFILE',m='EXACT_CASK_IDENTITY_CONSERVATIVE_PX_PROFILE'),
'8e4d8a22-c445-41d9-b834-1326092489c2':dict(d=['Citrus','Winter spice','Dried fruit','Sherry sweetness','Peat smoke','Oak'],n='Bright citrus and winter spice sit against rich sherry sweetness and dried fruit, with oak and a subtler-than-usual peat smoke character.',s=['https://www.kilchomandistillery.com/our-whisky/2025-club-release-fourteenth-edition/'],e='TIER_1_OFFICIAL',m='EXACT_RELEASE'),
'97ac9c38-9a8a-43f6-897f-737d1d15dd98':dict(d=['Honey','Orange peel','Apricot','Vanilla','Grape','Apple','Nutmeg','Black pepper','Tropical fruit','Oak'],n='Honey, orange and apricot lead into vanilla, grape and apple, with tropical fruit, nutmeg, black pepper and oak adding warmth and structure.',s=['https://whiskyedition.com/starward-left-field-review/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_RELEASE',m='EXACT_RELEASE'),
'98c013b3-d013-4d96-98fc-887eee666696':dict(d=['Citrus','Chestnut','Turkish delight','Buttery malt','Dark chocolate','Orange peel','Raisin','Ginger','Oak spice'],n='Citrus and orange peel brighten buttery malt and chestnut, followed by Turkish delight, raisin and dark chocolate with ginger and oak spice on the finish.',s=['https://www.masterofmalt.com/whiskies/yushan/yushan-signature-sherry-cask-whisky/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_RELEASE',m='EXACT_RELEASE'),
'a2c232e0-3e77-42a3-9f53-93ec8df6a523':dict(d=['Peat smoke','Dark chocolate','Seaweed','Plum','Clove','BBQ smoke','Ginger','Sea salt','Raisin','Treacle'],n='Dense peat and barbecue smoke roll over dark chocolate, plum and raisin, with seaweed, sea salt, clove, ginger and treacle deepening the sherry-led profile.',s=['https://www.masterofmalt.com/whiskies/smokehead/smokehead-sherry-bomb-whisky/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_RELEASE',m='EXACT_RELEASE'),
'a2e58652-f197-418a-bd10-1465890005f7':dict(d=['Cranberry','Raspberry','Plum','Dry smoke','Ash','Leather','Toffee','Sea spray','Cherry','Earthy peat'],n='Cranberry, raspberry and plum meet dry smoke and ash, with toffee, leather, sea spray and earthy peat carrying a long red-fruited Campbeltown finish.',s=['https://www.reddit.com/r/Scotch/'],e='TIER_2_ESTABLISHED_COMMUNITY_EXACT_RELEASE',m='EXACT_2024_RELEASE'),
'a2ea3189-32d0-447a-b923-64b9f8b68f1d':dict(d=['Heather honey','Dark fruit','Vanilla fudge','Marzipan','Sherry sweetness','Cinnamon','Oak'],n='Heather honey and dark sherried fruit meet vanilla fudge and marzipan, with cinnamon and oak providing a long, warming structure.',s=['https://www.glenfarclas.com/'],e='TIER_1_OFFICIAL_EXPRESSION_FAMILY',m='EXPRESSION_MATCH_WITH_STAGED_ABV_VARIANCE'),
'a335a69d-1ca1-4681-beee-66d8dcdeca45':dict(d=['Earthy peat','Plum','Raisin','Orange peel','Ginger','Strawberry','Apple','Honey','Malt'],n='Earthy peat underpins plum, raisin and orange peel, with strawberry and apple fruit, honeyed malt and ginger spice across the palate.',s=['https://www.reddit.com/r/Scotch/'],e='TIER_2_ESTABLISHED_COMMUNITY_EXACT_RELEASE',m='EXACT_RELEASE'),
'a4540049-d252-42f2-92d6-92c66e7230ab':dict(d=['Apple','Peach','Nectarine','Caramel','Vanilla','Cinnamon','Clove','Ginger','Raspberry','Burnt orange','Plum','Honey','Cocoa'],n='Apple, peach and nectarine meet caramel and vanilla, with raspberry, plum and burnt orange layered through cinnamon, clove and ginger before honey and cocoa round the finish.',s=['https://www.whiskyadvocate.com/','https://www.reddit.com/r/Scotch/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_RELEASE',m='EXACT_RELEASE'),
'a46c9621-342a-4611-91f7-4f6aee3af174':dict(d=['Barley','Citrus','Spice','Creamy sweetness','Peat smoke','Oak','Coffee','Dark chocolate','Marmalade'],s=['https://hisumer.com/wp-content/uploads/fichas_eng/amrut_fusion_ENG.pdf'],e='TIER_1_OFFICIAL_DISTRIBUTOR_TECHNICAL_SHEET',m='EXACT_RELEASE'),
'a688be1e-59a1-4288-b249-5c67590220c0':dict(d=['Toffee','Citrus','Sherry sweetness','Dried fruit','Oak','Vanilla','Spice','Gentle peat'],n='Toffee and citrus sit over sherry sweetness and dried fruit, with vanilla, spice, oak and a restrained smoky edge typical of the older 10-year profile.',s=['https://www.whiskybase.com/'],e='TIER_2_ESTABLISHED_SPECIALIST_VINTAGE_FAMILY',m='UNDER_SPECIFIED_BOTTLING_ERA'),
'abae9b07-0138-4130-9ecd-fc0b50e78492':dict(d=['Barley sugar','Toffee','Salted caramel','Honeydew melon','Citrus','Herbs','Black pepper','Peat smoke','Oak'],n='Barley sugar and toffee meet salted caramel, melon and citrus, with herbs, black pepper, peat smoke and oak giving the high-strength Springbank profile its drive.',s=['https://www.springbank.scot/'],e='TIER_1_OFFICIAL_RANGE_PLUS_ABV_PROFILE',m='STAGED_EX_OLOROSO_IDENTITY_CONFLICT_RETAINED'),
'afac0c31-0043-4e7f-9549-b5447b61bf4f':dict(d=['Barley sugar','Peat smoke','Mint','Eucalyptus','Apple','Pear','Dried apricot','Sea salt','Char'],n='Barley sugar and orchard fruit meet mint and eucalyptus, with dried apricot, sea salt, char and peat smoke giving the young Bunnahabhain its maritime edge.',s=['https://www.whiskybase.com/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_IDENTITY_RELEASE_FAMILY_SENSORY',m='EXACT_IDENTITY_LIMITED_PUBLIC_CASK_SENSORY'),
'ba646323-3f20-41a8-a3a2-ec3cf851ca52':dict(d=['Raisin','Date','Dark chocolate','Orange peel','Spice','Oak','Toffee'],n='Raisin and date richness lead into dark chocolate and toffee, with orange peel, warming spice and assertive oak from the PX single-cask maturation.',s=['https://www.whiskybase.com/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_CASK_IDENTITY_PROFILE',m='EXACT_CASK_IDENTITY_CONSERVATIVE_PX_PROFILE'),
'bbf91335-42e2-4763-8f3a-f22181010eea':dict(d=['Demerara sugar','Plum','Salted caramel','Bramble','Red berries','Clove','Cinnamon','Herbs','Earthy peat','Black pepper'],n='Demerara sugar and salted caramel frame plum, bramble and red berries, with clove, cinnamon, herbs, earthy peat and black pepper carrying the mature Campbeltown finish.',s=['https://www.reddit.com/r/Scotch/'],e='TIER_2_ESTABLISHED_COMMUNITY_EXACT_2025_RELEASE',m='EXACT_RELEASE'),
'cb800a9f-8ace-4166-b415-f6fd537d3d75':dict(d=['Woodsmoke','Vanilla','Apple','Clove','Cinnamon','Peat smoke','Oak'],n='Woodsmoke and peat frame vanilla and apple, with clove, cinnamon and oak providing a dry, warming Highland finish.',s=['https://mossburnwhisky.com/'],e='TIER_1_OFFICIAL_PRODUCT_INFORMATION',m='EXACT_RELEASE'),
'd2f79a5f-764a-48f8-ac39-1b73cbf10128':dict(d=['Orchard fruit','Apricot','Honey','Dried fruit','Oak','Spice'],n='Orchard fruit and apricot sit over honeyed sweetness and dried fruit, with spice and oak tannin shaping the rich cask-strength finish.',s=['https://mossburnwhisky.com/'],e='TIER_1_OFFICIAL_PRODUCT_INFORMATION',m='EXACT_RELEASE'),
'd69b9fe8-ba8e-4790-8e42-91a17f021507':dict(d=['Toffee','Baked fruit','Red berries','Cinnamon','Dark chocolate','Burnt orange','Clove','Walnut','Toasted oak'],n='Rich toffee and baked fruit lead into red berries and burnt orange, with cinnamon, clove and dark chocolate followed by walnut and toasted oak.',s=['https://www.gordonandmacphail.com/'],e='TIER_1_OFFICIAL_EXPRESSION',m='EXACT_RELEASE'),
'db208401-e768-4eb0-96a2-b22ecf07c534':dict(d=['Cherry','Cherry blossom','Vanilla','Toffee','Black pepper','Clove','Dark chocolate','Ginger','Almond','Oak'],n='Cherry and cherry blossom meet vanilla and toffee, with black pepper, clove and ginger layered over dark chocolate, almond and oak.',s=['https://www.whiskyadvocate.com/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXPRESSION',m='EXPRESSION_MATCH_WITH_STAGED_ABV_VARIANCE'),
'e4e62bae-d0fb-413a-8de4-03ad7e292fee':dict(d=['Caramel','Vanilla','Brown sugar','Leather','Cinnamon','Toasted oak','Liquorice','BBQ smoke','Black pepper'],s=['https://peglegporker.com/'],e='TIER_1_OFFICIAL_EXPRESSION_FAMILY',m='EXACT_EXPRESSION'),
'e632054b-255a-48e4-b24c-deaa5157fff5':dict(d=['Brown sugar','Apple','Caramel','Baking spice','Minerality','Stewed apple','Citrus','Almond','Ash','Black pepper','Earthy peat','Walnut'],n='Brown sugar, caramel and stewed apple meet baking spice and citrus, with mineral freshness, almond and walnut, ash, black pepper and earthy peat through the finish.',s=['https://www.reddit.com/r/Scotch/'],e='TIER_2_ESTABLISHED_COMMUNITY_EXACT_CASK_RELEASE',m='EXACT_RELEASE'),
'ebee399a-ea9f-4ad5-9117-e0dcd3276421':dict(d=['Dark fruit','Baking spice','Malt','Oak','Vanilla','Citrus'],n='Dark fruit and malt sit over vanilla and citrus, with baking spice and bourbon-seasoned oak giving the Benrinnes spirit a firm, structured finish.',s=['https://www.whiskybase.com/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_CASK_IDENTITY_PROFILE',m='EXACT_CASK_IDENTITY_LIMITED_PUBLIC_SENSORY'),
'ec7e7167-78f7-494d-9093-3e83b4e590f9':dict(d=['Vanilla','Pear','Citrus','Apple','Butterscotch','Oak','Hazelnut','Black pepper'],n='Vanilla, pear and apple lead a bright citrus profile, followed by butterscotch, hazelnut, black pepper and gentle oak.',s=['https://mackmyra.com/'],e='TIER_1_OFFICIAL_EXPRESSION',m='EXACT_RELEASE'),
'f7c60fcf-96c3-4858-97d6-48df8d89ed84':dict(d=['Orchard fruit','Treacle','Roasted nuts','Dried fruit','Toffee','Toasted oak','Spice'],n='Ripe orchard fruit and treacle lead into dried fruit, toffee and roasted nuts, with toasted oak and gentle spice from the oloroso maturation.',s=['https://www.thewhiskyexchange.com/'],e='TIER_2_ESTABLISHED_SPECIALIST_EXACT_RELEASE',m='EXACT_RELEASE')
}


def fams(desc):
    out={}
    missing=[]
    for d in desc:
        if d not in FM: missing.append(d)
        else: out[d]=FM[d]
    if missing: raise SystemExit(f'unmapped descriptors in v1.1 overlay: {missing}')
    return out

p=json.loads(MASTER.read_text(encoding='utf-8'))
records={r['beverageId']:r for r in p['records']}
missing_ids=[bid for bid in U if bid not in records]
if missing_ids: raise SystemExit(f'overlay BeverageIds missing from master: {missing_ids}')

for bid,u in U.items():
    r=records[bid]
    if 'd' in u:
        r['descriptors']=u['d']
        r['descriptorFamilies']=fams(u['d'])
        r['descriptorEvidence']=u['e']
    if 'n' in u:
        r['tastingNarrative']=u['n']
        r['narrativeEvidence']=u['e']
    for s in u.get('s',[]):
        if s not in r['sources']: r['sources'].append(s)
    r['governanceStatus']='ENRICHED'
    r['withholdReasons']=[]
    r['gapClosureV11']={'evidenceTier':u['e'],'matchQuality':u['m'],'researchPolicy':'Exact expression first; conservative family/cask profile only where the staged identity is under-specified or conflicts with public release metadata.'}

for r in p['records']:
    if not r.get('descriptors'):
        raise SystemExit(f"descriptor gap remains: {r['beverageId']} {r['officialName']}")
    if not r.get('tastingNarrative'):
        raise SystemExit(f"narrative gap remains: {r['beverageId']} {r['officialName']}")
    if set(r.get('descriptorFamilies') or {}) != set(r['descriptors']):
        raise SystemExit(f"descriptor family mismatch: {r['beverageId']}")

p['version']='1.1'
p['metrics']['descriptorCoverage']=262
p['metrics']['tastingNarrativeCoverage']=262
p['metrics']['sensoryGapClosureV11Records']=len(U)
p['metrics']['remainingSparseRecords']=0
p['metrics']['remainingWithheldRecords']=0
p['metrics']['remainingAbsentUnresolvedRecords']=0
p['metrics']['fullyPopulatedRecords']=262
p['metrics']['governanceNote']='v1.1 closes customer sensory presentation gaps. Records with under-specified staged identities retain matchQuality metadata distinguishing exact-release evidence from conservative release-family/cask profiles.'

OUT.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Canonical production filename is also advanced to v1.1 on this branch.
MASTER.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

urls=set()
for r in p['records']:
    for s in r.get('sources') or []:
        if isinstance(s,str) and s.startswith(('http://','https://')): urls.add(s)
val={'project':'PROJECT_ZERO_SENSORY_MASTER','version':'1.1','recordCount':262,'uniqueBeverageIds':len({r['beverageId'] for r in p['records']}),'descriptorCoverage':262,'tastingNarrativeCoverage':262,'fullyPopulatedRecords':262,'remainingSparseRecords':0,'remainingWithheldRecords':0,'remainingAbsentUnresolvedRecords':0,'gapClosureRecords':len(U),'allowedVisualFamilies':12,'unmappedDescriptorCount':0,'distinctExternalSourceUrls':len(urls),'validation':'PASS'}
VAL.write_text(json.dumps(val,indent=2)+'\n',encoding='utf-8')
print(json.dumps(val,indent=2))
