package edu.umn.cs.recsys.uu;

import it.unimi.dsi.fastutil.longs.LongSet;
import org.grouplens.lenskit.basic.AbstractItemScorer;
import org.grouplens.lenskit.data.dao.ItemEventDAO;
import org.grouplens.lenskit.data.dao.UserEventDAO;
import org.grouplens.lenskit.data.event.Rating;
import org.grouplens.lenskit.data.history.History;
import org.grouplens.lenskit.data.history.RatingVectorUserHistorySummarizer;
import org.grouplens.lenskit.data.history.UserHistory;
import org.grouplens.lenskit.vectors.MutableSparseVector;
import org.grouplens.lenskit.vectors.SparseVector;
import org.grouplens.lenskit.vectors.VectorEntry;
import org.grouplens.lenskit.vectors.similarity.CosineVectorSimilarity;

import javax.annotation.Nonnull;
import javax.inject.Inject;
import java.util.*;

/**
 * User-user item scorer.
 * @author <a href="http://www.grouplens.org">GroupLens Research</a>
 */
public class SimpleUserUserItemScorer extends AbstractItemScorer {
    private final UserEventDAO userDao;
    private final ItemEventDAO itemDao;

    @Inject
    public SimpleUserUserItemScorer(UserEventDAO udao, ItemEventDAO idao) {
        userDao = udao;
        itemDao = idao;
    }

    /* Comparator to sort the <user, similarity map and find top 30 */
    class ValueComparator implements Comparator<Long> {

        Map<Long, Double> base;
        public ValueComparator(Map<Long, Double> base) {
            this.base = base;
        }

        @Override
        public int compare(Long a, Long b) {
            if (base.get(a) >= base.get(b)) {
                return -1;
            } else {
                return 1;
            } // returning 0 would merge keys
        }
    }

    /* Return Top 30 Neighbors for USER user based on an item item ID) */
    private TreeMap<Long, Double> getTop30Neighbors(long user,long itemID)
    {
        SparseVector userVector = getUserRatingVector(user);
        MutableSparseVector userVectorCentered = userVector.mutableCopy(); /* Get centered rating vector */
        userVectorCentered.add( -userVectorCentered.mean() );

        LongSet possibleNeighbors = itemDao.getUsersForItem(itemID); // These are all the neighbors
        TreeMap<Long, Double> neighborSimilarityMap = new TreeMap<Long, Double>();
        ValueComparator bvc =  new ValueComparator(neighborSimilarityMap); // To sort the user->similarity mapping
        TreeMap<Long, Double> sortedNeighbors = new TreeMap<Long,Double>(bvc);

        for (Long u: possibleNeighbors) {
            SparseVector possibleNeighborVector = getUserRatingVector(u);
            MutableSparseVector possibleNeighborVectorCentered = possibleNeighborVector.mutableCopy();
            possibleNeighborVectorCentered.add( -possibleNeighborVectorCentered.mean() );

            // Compute the similarity between our user and a neighbor
            CosineVectorSimilarity cvs = new CosineVectorSimilarity();
            double similarity = cvs.similarity(userVectorCentered, possibleNeighborVectorCentered);
            if (u != user) {
                neighborSimilarityMap.put(u, similarity); // add to neighbor->similarity map
            }
        }

        sortedNeighbors.putAll(neighborSimilarityMap);
        neighborSimilarityMap.clear(); // Clear the map
        Iterator it = sortedNeighbors.entrySet().iterator();
        int i = 0;
        /* Now select the TOP 30 neighbors */
        while (it.hasNext() && i++ < 30) {
            Map.Entry pairs = (Map.Entry)it.next();
            neighborSimilarityMap.put((Long)pairs.getKey(), (Double)pairs.getValue());
        }

        return neighborSimilarityMap;  // Return the TOP 30 neighbors
    }

    /* Score an item itemID for USER user */
    private double getScore(long user, TreeMap<Long, Double> top30Neighbors, long itemID) {
        double score = 0.0;

        SparseVector userVector = getUserRatingVector(user);
        MutableSparseVector userVectorCentered = userVector.mutableCopy();
        Double userMean = userVector.mean();

        double denominator = 0.0;
        Iterator it = top30Neighbors.entrySet().iterator();
        /* Iterate over all neighbors */
        while (it.hasNext()) {
            Map.Entry n_s = (Map.Entry)it.next();
            long neighbor = (Long)n_s.getKey();
            double sim = (Double)n_s.getValue();

            SparseVector neighborVector = getUserRatingVector(neighbor);
            double neighborMean = neighborVector.mean();
            double rating = neighborVector.get(itemID);

            score += sim * (rating - neighborMean);
            denominator += Math.abs(sim);
        }

        /* Compute the score */
        score = userMean + score / denominator;

        return score;
    }

    @Override
    public void score(long user, @Nonnull MutableSparseVector scores) {
        // TODO Score items for this user using user-user collaborative filtering

        // This is the loop structure to iterate over items to score
        for (VectorEntry e: scores.fast(VectorEntry.State.EITHER)) {
            /* First, get top 30 neighbors */
            TreeMap<Long, Double> top30Neighbors = getTop30Neighbors(user, e.getKey());
            /* Get score for an item */
            double score = getScore(user, top30Neighbors, e.getKey());
            scores.set(e.getKey(), score);
        }
    }

    /**
     * Get a user's rating vector.
     * @param user The user ID.
     * @return The rating vector.
     */
    private SparseVector getUserRatingVector(long user) {
        UserHistory<Rating> history = userDao.getEventsForUser(user, Rating.class);
        if (history == null) {
            history = History.forUser(user);
        }
        return RatingVectorUserHistorySummarizer.makeRatingVector(history);
    }
}







***************************************SECOND**********************************




package edu.umn.cs.recsys.uu;

import java.util.Map;

import it.unimi.dsi.fastutil.doubles.DoubleSortedSet;
import it.unimi.dsi.fastutil.doubles.DoubleSortedSets;

import javax.annotation.Nonnull;
import javax.inject.Inject;

import org.grouplens.lenskit.basic.AbstractItemScorer;
import org.grouplens.lenskit.data.dao.ItemEventDAO;
import org.grouplens.lenskit.data.dao.UserEventDAO;
import org.grouplens.lenskit.data.event.Rating;
import org.grouplens.lenskit.data.history.History;
import org.grouplens.lenskit.data.history.RatingVectorUserHistorySummarizer;
import org.grouplens.lenskit.data.history.UserHistory;
import org.grouplens.lenskit.transform.truncate.TopNTruncator;
import org.grouplens.lenskit.vectors.MutableSparseVector;
import org.grouplens.lenskit.vectors.SparseVector;
import org.grouplens.lenskit.vectors.VectorEntry;
import org.grouplens.lenskit.vectors.similarity.CosineVectorSimilarity;

import com.google.common.collect.Maps;

/**
 * User-user item scorer.
 * @author <a href="http://www.grouplens.org">GroupLens Research</a>
 */
public class SimpleUserUserItemScorer extends AbstractItemScorer {
    private final UserEventDAO userDao;
    private final ItemEventDAO itemDao;

    @Inject
    public SimpleUserUserItemScorer(UserEventDAO udao, ItemEventDAO idao) {
        userDao = udao;
        itemDao = idao;
    }

    @Override
    public void score(long user, @Nonnull MutableSparseVector scores) {
        SparseVector userVector = getUserRatingVector(user);

        // Create a mutable copy of the userVector to compute the user mean-centered rating vector
        MutableSparseVector userMeanCenteredRatingVector = userVector.mutableCopy();
        userMeanCenteredRatingVector.add(-userVector.mean());

        // This is the loop structure to iterate over items to score
        for (VectorEntry e: scores.fast(VectorEntry.State.EITHER)) {
            // Create a map to store the user similarities
            Map<Long, Double> userSimilarities = Maps.newHashMap();
            double similarity;

            // Create a map to store the neighbor vectors
            Map<Long, SparseVector> neighborVectors = Maps.newHashMap();
            
            // Get the list of users who have rated the item to score
            for (Long neighbor : itemDao.getUsersForItem(e.getKey())) {
                // Do not calculate similarity against itself
                if (neighbor == user) {
                    continue;
                }
                
                // Add the neighbor vector to the map of neighbor vectors
                neighborVectors.put(neighbor, getUserRatingVector(neighbor));
                
                // Create the neighbor mean-centered rating vector
                MutableSparseVector neighborMeanCenteredRatingVector = neighborVectors.get(neighbor).mutableCopy();
                neighborMeanCenteredRatingVector.add(-neighborVectors.get(neighbor).mean());
                
                // Compute user similarities by taking the cosine between both (user and neighbor) mean-centered rating vectors
                similarity = new CosineVectorSimilarity().similarity(userMeanCenteredRatingVector, neighborMeanCenteredRatingVector);
                userSimilarities.put(neighbor, similarity);
            }

            double sUV = 0;
            double rVI = 0;
            double uV = 0;
            double dividend = 0;
            double divisor = 0;
            
            // Get the top 30 most similar neighbors (couldn't find a better way to do that :'( )
            MutableSparseVector neighbors = MutableSparseVector.create(userSimilarities);
            for (Long neighbor : neighbors.keysByValue(true).longSubList(0, 30)) {
                
                // Similarity between users U (user) and V (neighbor)
                sUV = userSimilarities.get(neighbor);
                // Rate of user V (neighbor) for item I (item to score)
                rVI = neighborVectors.get(neighbor).get(e.getKey());
                // User V (neighbor) average rating
                uV = neighborVectors.get(neighbor).mean();
                dividend += sUV * (rVI - uV);
                // Absolute value of similarity between users U (user) and V (neighbor)
                divisor += Math.abs(sUV);
            }
            
            // Set score to item
            scores.set(e.getKey(), userVector.mean() + (dividend/divisor));
        }
    }

    /**
     * Get a user's rating vector.
     * @param user The user ID.
     * @return The rating vector.
     */
    private SparseVector getUserRatingVector(long user) {
        UserHistory<Rating> history = userDao.getEventsForUser(user, Rating.class);
        if (history == null) {
            history = History.forUser(user);
        }
        return RatingVectorUserHistorySummarizer.makeRatingVector(history);
    }
}
