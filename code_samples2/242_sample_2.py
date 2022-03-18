        if 'softmax' in args.config:
            f1, acc, prec, recall = score(preds, targets)
            logger.info("Valid at epoch {0}, F1:{1:.3f}, Acc:{2:.3f}, P:{3:.3f}, R:{4:.3f}, Loss:{5:.3f}"\
                    .format(epoch, f1, acc, prec, recall, valid_loss))
            f1s.append((f1, 0.5))
        else:
            for threshold in np.arange(0.45, 0.85, 0.01):
                f1, acc, prec, recall = score(preds, targets, threshold=threshold)
                logger.info("Valid at epoch {0}, threshold {6}, F1:{1:.3f}, Acc:{2:.3f}, P:{3:.3f}, R:{4:.3f}, Loss:{5:.3f}"\
                        .format(epoch, f1, acc, prec, recall, valid_loss, threshold))
                f1s.append((f1, threshold))
            print()