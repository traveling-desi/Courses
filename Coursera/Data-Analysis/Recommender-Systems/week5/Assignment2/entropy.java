


// Get all the unique tags present in the 10 movies recommended
MutableSparseVector tagVector = vocab.newTagVector()



//// recommendations is List<ScoreId>
for (ScoreId movie: recommendations) {
	
	/// set up a hash for unique tags for THIS movie
	Set<String> uniqueMovieTags = Sets.newHashSet();
	List<String> movie_tags = tagDAO.getItemTags(movie.getId());
	for (String tag: movie_tags) {
		String normed = tag.toLowerCase();
		if (!uniqueMovieTags.contains(normed)) {
		    uniqueMovieTags.add(normed);
		}
	}

	int tagSize = uniqueMovieTags.size()

	/// How do I get the keyset for all teh unique tags for 
	foreach keys in uniqueMovieTags {





		
		long tagId = vocab.getTagId(tag);

		if (tagVector.containsKey(tagId)) {
                double value = tagVector.get(tagId);
                tagVector.add(tagId, value + (1.0 / (double) (tagSize)));
        } else {
                tagVector.set(tagId, 1.0 / (double) (tagSize));
        }
    }

}